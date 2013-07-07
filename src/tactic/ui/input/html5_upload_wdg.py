###########################################################
#
# Copyright (c) 2005-2012, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#


__all__ = ['Html5UploadWdg', 'UploadButtonWdg', 'CheckinButtonWdg', 'TestHtml5UploadWdg']

from tactic.ui.common import BaseRefreshWdg

from pyasm.common import Common
from pyasm.web import HtmlElement, DivWdg
from pyasm.widget import TextWdg, HiddenWdg


class Html5UploadWdg(BaseRefreshWdg):

    def init(my):

        name = my.kwargs.get("name")
        if not name:
            name = "table_upload"

        my.form = HtmlElement.form()

        my.form_id = my.kwargs.get("upload_id")
        if my.form_id:
            my.form.set_id(my.form_id)
        else:
            my.form_id = my.form.set_unique_id(name)


    def get_upload_id(my):
        return my.form_id

    def get_display(my):

        top = my.top
        form = my.form
        form.add_style("margin: 0px")
        form.add_style("padding: 0px")


        top.add(form)

        input = HtmlElement.input()
        form.add(input)
        input.set_attr("name", "file")
        input.add_class("spt_file")
        input.set_attr("type", "file")
        #input.add_style("display: none")
        #input.add_style("visibility: hidden")
        input.add_style("position: absolute")
        input.add_style("margin-left: -5000px")


        form.add_behavior( {
            'type': 'load',
            'cbjs_action': '''
spt.html5upload = {};
spt.html5upload.form = null;
spt.html5upload.files = [];
spt.html5upload.events = {};


spt.html5upload.set_form = function(form) {
    if (!form) {
        spt.alert('Cannot initialize the HTML upload. Invalid form detected.');
        return;
    }
    spt.html5upload.form = form;
}

// get the last one in the list since this FileList is readonly and it is additive if multiple attr is on
spt.html5upload.get_file = function() {
    var files = spt.html5upload.get_files();
    if (files.length == 0) {
        return null;
    }
    return files[files.length-1];
}


//FIXME: it doesn't need to be stored as files since it should be called
// every time an upload occurs
spt.html5upload.get_files = function() {
    var file_input = spt.html5upload.form.getElement('.spt_file');
    spt.html5upload.files = file_input.files;
    return spt.html5upload.files;
}


spt.html5upload.select_file = function(onchange) {
    var files = spt.html5upload.select_files(onchange);
    if (!files) {
        spt.alert('You may need to refresh this page.');
        return null;
    }
        
    if (files.length == 0) {
        return null;
    }
    return files[0];
}


spt.html5upload.select_files = function(onchange) {
    var form = spt.html5upload.form;
    if (!form) {
        spt.alert('Cannot locate the upload form. Refresh this page/tab and try again');
        return; 
    }

    var el = form.getElement(".spt_file") ;
  
    // ensure this listener is only added once
    if (!spt.html5upload.events['select_file']){
        el.addEventListener("change", onchange, true);
    }

    // This is necessary for Qt on a Mac??
    if (spt.browser.is_Qt() || spt.browser.is_Safari()) {
        setTimeout( function() {
            el.click();
            spt.html5upload.events['select_file'] = onchange;
        }, 100 );
    }
    else {
        el.click();
        spt.html5upload.events['select_file'] = onchange;
    }

    // FIXME: this is not very useful as the select file is async, but
    // is required for later code not to opne a popup
    spt.html5upload.files = el.files;
    return spt.html5upload.files;
}

// clears the otherwise readonly filelist, disables the input
spt.html5upload.clear = function() {
    var form = spt.html5upload.form;
    var el = form.getElement(".spt_file");
    el.value = null;
    
    // cloning clears all the event listeners
    var new_element = el.cloneNode(true);
    el.parentNode.replaceChild(new_element, el);

    spt.html5upload.events['select_file'] = null;
    
}


spt.html5upload.upload_failed = function(evt) {
    spt.app_busy.hide();
    spt.alert("Upload failed");
}


spt.html5upload.upload_file = function(kwargs) {

  if (!kwargs) {
      kwargs = {};
  }

  var xhr = new XMLHttpRequest();
  var form = spt.html5upload.form;
  var el = form.getElement(".spt_file") ;
  var file_name = el.value;
  if (file_name.test(/,/)) {
      spt.alert('Comma , is not allowed in file name.');
      spt.html5upload.clear();
      return;
  }

  var upload_start = kwargs.upload_start;
  var upload_complete = kwargs.upload_complete;
  var upload_progress = kwargs.upload_progress;
  var upload_failed = spt.html5upload.upload_failed;
  var transaction_ticket = kwargs.ticket;
  //var fd = form.getFormData();
  var fd = new FormData(form);
  if (transaction_ticket) {
      fd.append('transaction_ticket', transaction_ticket);
  }

  /* event listeners */
  if (upload_start) {
      xhr.upload.addEventListener("loadstart", upload_start, false);
  }
  if (upload_progress) {
      xhr.upload.addEventListener("progress", upload_progress, false);
  }
  if (upload_complete) {
      xhr.addEventListener("load",  upload_complete, false);
  }
  if (upload_failed) {
      xhr.addEventListener("error", upload_failed, false);
  }
  //xhr.addEventListener("abort", uploadCanceled, false);
  xhr.open("POST", "/tactic/default/UploadServer/", true);
  xhr.send(fd);

}


        '''
        } )


        return top




class UploadButtonWdg(BaseRefreshWdg):

    def init(my):
        my.on_complete = my.kwargs.get("on_complete")
        my.ticket = my.kwargs.get("ticket")
        super(UploadButtonWdg,my).init()


    def set_on_complete(my, on_complete):
        my.on_complete = on_complete

    def get_on_complete(my):
        return my.on_complete


    def get_display(my):

        top = my.top
        top.add_class("spt_upload_top")

        title = my.kwargs.get("title")
        name = my.kwargs.get("name")

        if not name:
            name = "upload"

        if not title:
            title = Common.get_display_title(name)

        search_key = my.kwargs.get("search_key")


        hidden = HiddenWdg(name)
        top.add(hidden)


        upload = Html5UploadWdg(name=name)
        top.add(upload)
        upload_id = upload.get_upload_id()

        from tactic.ui.widget import ActionButtonWdg
        button = ActionButtonWdg(title=title)
        button_id = my.kwargs.get("id")
        if button_id:
            button.set_id(button_id)
        top.add(button)


        on_complete = my.get_on_complete()

        if not on_complete:
            on_complete = '''
            var file = spt.html5upload.get_file();
            if (!file) {
               alert('Error: file cannot be found.')
               spt.app_busy.hide();
               return;
            }

            file_name = file.name;
            spt.notify.show_message(file_name);
            spt.app_busy.hide();
            '''


        button.add_behavior( {
            'type': 'click_up',
            'upload_id': upload_id,
            'search_key': search_key,
            'ticket': my.ticket,
            'cbjs_action': '''
            var search_key = bvr.search_key;

            // set the form
            spt.html5upload.form = $(bvr.upload_id);

            // set an action for completion
            var upload_complete = function(evt) {
            %s;
            spt.app_busy.hide();
            }

            var upload_start = function(evt) {
                var top = bvr.src_el.getParent(".spt_upload_top");
                var hidden = top.getElement(".spt_input");
                var file = spt.html5upload.get_file();
                if (!file) {
                   return;
                }
                hidden.value = file.name;
            }

            var percent_complete = function(evt) {
                var percent = Math.round(evt.loaded * 100 / evt.total);
                spt.app_busy.show("Uploading ["+percent+"%% complete]");
            } 

            var upload_file_kwargs =  {
                  upload_start: upload_start,
                  upload_complete: upload_complete,
                  upload_progress: percent_complete 
                };
            if (bvr.ticket)
               upload_file_kwargs['ticket'] = bvr.ticket; 
                

	    var onchange = function () {
                spt.html5upload.upload_file(upload_file_kwargs);
	    }

            spt.html5upload.select_file( onchange);

            ''' % on_complete
        } )

        return top



class CheckinButtonWdg(UploadButtonWdg):

    def get_on_complete(my):

        context = my.kwargs.get("context")
        if not context:
            context = 'publish'

        return '''
            var server = TacticServerStub.get();
            var file = spt.html5upload.get_file();
            if (file) {
               file_name = file.name;
                 
               server.simple_checkin(search_key, "%s", file_name, {mode:'uploaded', checkin_type:'auto'});
               spt.notify.show_message("Check-in of ["+file_name+"] successful");
            }
            else  {
              alert('Error: file object cannot be found.')
            }
            spt.app_busy.hide();
        ''' % context






class TestHtml5UploadWdg(BaseRefreshWdg):

    def get_display(my):

        top = my.top

        upload = Html5UploadWdg(name="formxyz")
        top.add(upload)
        upload_id = upload.get_upload_id()

        from tactic.ui.widget import ActionButtonWdg
        button = ActionButtonWdg(title="Upload")
        top.add(button)
        button.add_behavior( {
            'type': 'click_up',
            'upload_id': upload_id,
            'cbjs_action': '''

            // set the form
            spt.html5upload.form = $(bvr.upload_id);

            // set an action for completion
            var upload_complete = function(evt) {
                var search_key = "sthpw/login?code=admin";
                var server = TacticServerStub.get();
                var file = spt.html5upload.get_file();
                if (file) {
                   file_name = file.name;
                     
                   server.simple_checkin(search_key, "icon", file_name, {mode:'uploaded'});
                }
                else 
                  alert('Error: file object cannot be found.')

            }

            var percent_complete = function(evt) {
                var percent = Math.round(evt.loaded * 100 / evt.total);
            }

	    var onchange = function () {
                spt.html5upload.upload_file( {
                  upload_complete: upload_complete,
                  upload_progress: percent_complete 
                } );
	    }


	
            spt.html5upload.select_file( onchange);

            '''
        } )

        return top





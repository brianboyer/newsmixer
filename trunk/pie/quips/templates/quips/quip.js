if (NM === undefined) {
  var NM = new function() {};
}

NM.Quips = new function() {
  var self=this;
  this.quipRefresh = 0;
  this.curdate = "{% now "Y-m-d H:i:s" %}";
  this.quipLimit = {% firstof limit '0' %};
  
  this.stopLive = function() {
    clearInterval(this.quipRefresh);
    window.onblur = '';
  };
  
  this.makeLive = function() {
  	clearInterval(this.quipRefresh);
    this.loadQuips();
  	this.quipRefresh = setInterval("NM.Quips.loadQuips()",12000);
  	window.onblur = this.stopLive;
  	window.onfocus = this.makeLive;
  };

  this.init = function() {
  	NM_$('#quip-form').ajaxForm({
  		dataType:'json',
  		beforeSubmit:function(){
  			self.stopLive();
  			return true;
  		},
  		success:self.pushToFacebookFeedAndInsert,
  		url:"/quips/create/remote"
  	});
  	this.makeLive();
  };

  this.pushToFacebookFeedAndInsert = function(data){
  	NM_Quips_makeLive();
  	if(data['success']){
  		NM_$('#quip-form').resetForm();
  		NM_$('.charsLeft').text('140');
  		var template_data = data['template_data'];
  		var template_bundle_id = data['template_bundle_id'];
  		//feedTheFacebook(template_data,template_bundle_id);
  	} else {
  		alert(data['errors']);
  	}
  };

  this.loadQuips = function() {
    
  	NM_$.post('/quips/',
  	          {'since':this.curdate,
  	           'show_headline':false,
  	           'article_url':window.location.href},
  	          function(data,textStatus){                
                if(data['insert'] != null){
                  newStuff = NM_$("#NM-quip-body").prepend(data['insert']);
                  NM_$("#NM-quip-body").find('#start-message').remove();
                  newStuff
                      .children(':first')
                      .css('backgroundColor','yellow')
                      .animate({'backgroundColor':'#fdfcf7'},2000);
                    
                }
              	self.curdate = data['date'];
               },
               "json");
  	
  	if ( this.quipLimit > 0 ){
  	  while ( NM_$('#NM-quip-body .quip').length > this.quipLimit )
  		  NM_$('#NM-quip-body .quip:last').remove();
  	}
  };

  this.initForm = function() {
    if ( NM_$('#quip-form textarea#id_message').length > 0 )
    	NM_$('#quip-form textarea#id_message').maxlength({ 
    		'feedback' : '.charsLeft',
    		'useInput' : true
    	});
  };
  
  this.settings = function(settingsObj) {
    for (var i in settingsObj)
      this[i] = settingsObj[i];
  };
}

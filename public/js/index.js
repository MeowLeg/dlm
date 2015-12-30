$(function() {
	$.hg_h5app({
		"needUserInfo": function(d) {
			var _callAjax = _genCallAjax("http://develop.zsgd.com:11011/dlm/");
			// var _callAjax = _genCallAjax("http://60.190.176.77:7023/dlm/");
			_callAjax({
				"cmd":"authorize"
			}, function(d) {
				var cnt = 0,
						tmpl = '<div class="alicance-frame">';
				d.data.tokens.forEach(function(r) {
					var k = r[0], title = r[1];
					cnt += 1;
					if (cnt > 3) cnt = cnt%3;

					tmpl += '<div class="alicance-icon space-top"><a href="list.html?key='+k+'"><img src="img/'+k+'.jpg" /><h6>'+title+'</h6></a></div>';
					if (cnt == 3) {
						$(".copyright").before(tmpl+"</div>");
						tmpl = '<div class="alicance-frame">';
					}

				});
				while (cnt < 3) {
					cnt += 1;
					tmpl += '<div class="alicance-icon space-top"></div>';
				}
				$(".copyright").before(tmpl+"</div>");
			});
		}
	});
});

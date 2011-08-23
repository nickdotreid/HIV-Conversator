$(document).ready(function(){
	$("#graph").bind('fetch',function(event){
		bar = $(".bar.loading:first",$(this))
		date = bar.data("date")
		$(".date",bar).html((date.getMonth()+1)+"/"+date.getDate())
		$.ajax({
			url:"/tweets",
			type:'post',
			dataType:'json',
			data:{
				day:date.getDate(),
				month:date.getMonth()+1,
				year:date.getFullYear()
			},
			success:function(data){
				bar.removeClass("loading");
				if(data['total']>0){
					bar.data("total",data['total'])
					$("#graph").trigger("draw")
				}
				$("#graph").trigger("fetch")
			}
		})
	}).bind("add",function(event){
		$("#templates .bar").clone().data("total",0).data("date",event.date).addClass("loading").appendTo($("#graph"));
	}).bind("draw",function(event){
		graph = $(this)
		$(".bar .canvas",graph).remove()
		bars = $(".bar",graph)
		max = 0;
		for(var i=0;i<bars.length;i++){
			bar = $(bars[i])
			if(bar.data("total")>max){
				max = bar.data("total")
			}
		}
		if(max >0){
			for(var i=0;i<bars.length;i++){
				bar = $(bars[i])
				bar.prepend("<div class='canvas'></div>")
				height = (bar.data('total')/max)*graph.height()
				$('.canvas',bar).height(height).css("top",(graph.height()-height)+"px");
			}
		}
	});
	date = new Date()
	day_in_milliseconds = 86400000
	limit = new Date(date.getTime()-(day_in_milliseconds*40))
	while(date>=limit){
		$("#graph").trigger({
			type:'add',
			date:date
		});
		date = new Date(date.getTime()-day_in_milliseconds)
	}
	$("#graph").trigger("fetch")
})
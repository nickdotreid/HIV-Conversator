$(document).ready(function(){
	$("#graph").bind('fetch',function(event){
		date = event.date
		$.ajax({
			url:"/tweets",
			type:'post',
			dataType:'json',
			data:{
				date:date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getYear()
			},
			success:function(data){
				if(data['tweets']){
					// add new bar
					$("#graph").trigger({
						type:"fetch",
						date:new Date(event.date.getTime()-86400000)
					})
				}
			}
		})
	}).trigger({
		type:'fetch',
		date:new Date()
	})
})
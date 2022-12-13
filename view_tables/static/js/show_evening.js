function player_arrived(player){
    var player_id = $(player).attr('player_id');
    var checked = player.checked;
    var arrived = 0;


    var url = '/view_tables/update_arrival/' + player_id + '/' + checked;
    csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(url,{
	method:'POST',
	headers:{
	    'X-Requested-With':'XMLHttpRequest',
	    'X-CSRFToken': csrftoken,
	}
    })
	.then (response=>response.json())
	.then (data => {
	    $("#tot_reg").innerHTML = data['tot_regs'];
	    $("#tot_arrived")[0].innerText = data['tot_arrived'];

	})

}

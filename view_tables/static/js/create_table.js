function toggle_number_of_players_field(){
    limit_num = document.getElementById('limit_number_of_players');
    max_num_field = document.getElementById('max_number_of_player_row');
    if (limit_num.checked){
	max_num_field.removeAttribute('hidden');
    }else{
	max_num_field.setAttribute('hidden','true');
    }
}

function check_fields(){
    document.getElementById('error').innerHTML = '';
    document.getElementById('submit').removeAttribute('disabled');
    is_dnd5 = document.getElementById('is_dnd5').checked;
    limit_num = document.getElementById('limit_number_of_players').checked;

    min_level = document.getElementById('min_level').value;
    max_level = document.getElementById('max_level').value;
    max_players = document.getElementById('max_number_of_players').value;

    min_level_val = parseInt(min_level);
    max_level_val = parseInt(max_level);
    max_players = parseInt(max_players);


    
    error = '';
    if (Number.isNaN(min_level_val) && is_dnd5){
	error = 'Please select a minium level<br>';
    }else if ((min_level <= 0 || min_level >= 20) && is_dnd5){
	error = 'Please select a minimum level between 1 and 19<br>';
    }

    if (Number.isNaN(max_players) && limit_num){
	error = error + 'Please set maximum number of players or remove the request to players limit<br>';
    }

    if (Number.isNaN(max_level_val) && is_dnd5){
	error = error+ 'Please select a maximum level<br>';
    }else if ((max_level <= 1 || max_level > 20) && is_dnd5){
	error = error + 'Plase select a maximum level between 2 and 20';
    }

    if (min_level_val > max_level_val && is_dnd5){
	error = 'Plaese select minium level that is smaller than maximum level';
    }



    


    if (error != ''){
	document.getElementById('submit').setAttribute('disabled','true');
    }

    document.getElementById('error').innerHTML = error;

    

}

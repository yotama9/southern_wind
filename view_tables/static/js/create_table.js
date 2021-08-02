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
    is_dnd5 = document.getElementById('is_dnd5').checked;
    if (!is_dnd5){
	return;
    }
    min_level = document.getElementById('min_level').value;
    max_level = document.getElementById('max_level').value;

    min_level_val = parseInt(min_level);
    max_level_val = parseInt(max_level);
    error = ''
    if (Number.isNaN(min_level_val)){
	error = 'Please select a minium level<br>';
    }else if (min_level <= 0 || min_level >= 20){
	error = 'Please select a minimum level between 1 and 19<br>';
    }if (Number.isNaN(max_level_val)){
	error = error+ 'Please select a maximum level<br>';
    }else if (max_level <= 1 || max_level > 20){
	error = error + 'Plase select a maximum level between 2 and 20';
    }if (min_level_val > max_level_val){
	error = 'Plaese select minium level that is smaller than maximum level';
    }

    document.getElementById('error').innerHTML = error;

    

}

function check_fields(){
    document.getElementById('submit').removeAttribute('disabled');
    error = "";
    if (document.getElementById('id_player').value == ""){
	error = error + "Please add your name to the form<br>";
    }

    if (document.getElementById('id_adventure').value == -1){
	error = error + "Please select an adventure to register to<br>";
    }

    has_char = document.getElementById('id_I_already_have_a_character').checked;
    char_level = document.getElementById('id_character_level').value
    
    if (has_char){
	if (char_level == ''){
	    error = error + "Please add your character level<br>";
	}
    }

    if (error != ''){
	document.getElementById('submit').setAttribute('disabled','true');
    }

    document.getElementById('error').innerHTML = error;
}


function toggle_character_level_field(){
    if (document.getElementById('id_I_already_have_a_character').checked){
	document.getElementById('id_character_level').removeAttribute('disabled');
    }else{
	document.getElementById('id_character_level').setAttribute('disabled','true');
	document.getElementById('id_character_level').value = '';
    }
}

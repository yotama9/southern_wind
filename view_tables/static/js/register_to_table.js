import { get_csrf } from './module.js';


$(document).ready(function(){
    $('#form').on('submit', function(e) {
	e.preventDefault();
	submit_register(e);
    });

    $("#form").on('mouseover',function(e){
	check_fields()
    });
    
    //$('#form').ajaxForm(function(){
    //$("#submit").addClass('button--clicked').removeClass('register-button');
    //$("#submit").text('Thank you');
    //$("#submit").prop('disabled','true');
//});
    
});

function submit_register(e){
    e.preventDefault();

    $("#submit").prop('disabled','true');
    console.log("not submitted");
    //creating the ajax call
    var url = window.location.pathname;
    console.log(url);
    var name = $('#id_player_name').val();
    var dnd = $('#id_non_DnD').val();
    $.ajax({
	url:url,
	type:'POST',
	data: {
	    player_name : name,
	    non_dnd : dnd,
	},
	headers:{
	    'X-CSRFToken':get_csrf(),
	},
	success: function(json_in){
	    $("#submit").addClass('button--clicked').removeClass('register-button');
	    $("#submit").text('Thank you');
	    $("#submit").prop('disabled','true');
	},
	error : function(xhr,errmsg,err) {
	    console.log('error');
	},
    })
}




function check_fields(){
    return;
    document.getElementById('submit').removeAttribute('disabled');

    var error = "";
    if (document.getElementById('id_player').value == ""){
	error = error + "Please add your name to the form<br>";
    }

    if (document.getElementById('id_adventure').value == -1){
	error = error + "Please select an adventure to register to<br>";
    }

    var has_char = document.getElementById('id_I_already_have_a_character').checked;
    var char_level = document.getElementById('id_character_level').value
    var char_name = document.getElementById('id_character_name').value

    /*Getting the selected adventure */
    var select = document.getElementById('id_adventure');
    var adventure = select.options[select.selectedIndex].value;
    var min_level = document.getElementById(adventure+"_min_level").getAttribute("value");
    var max_level = document.getElementById(adventure+"_max_level").getAttribute("value");

    
    if (has_char){
	if (char_level == ''){
	    error = error + "Please add your character level<br>";
	} else if (min_level != "None" && char_level < min_level){
	    error = error + "Character level is too low<br>";
	} else if (max_level != "None" && char_level > max_level){
	    error = error + "Character level is too high<br>";
	}

	if (char_name == ''){
	    error = error + "Please write your character name<br>";
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
	document.getElementById('id_character_name').removeAttribute('disabled');
    }else{
	document.getElementById('id_character_level').setAttribute('disabled','true');
	document.getElementById('id_character_name').setAttribute('disabled','true');
	document.getElementById('id_character_level').value = '';
    }
}



function isFormHtml5Valid(form){
    console.log(form);
}



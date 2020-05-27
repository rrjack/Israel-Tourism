/*
function validation(){
    var result = true;
    var i = document.getElementsByTagName("input");
    for(j=0;j<=5;j++){
        if(i[j].value.length==0){
            result = false;
            alert("one or more fields are empty");
            break;
        }
    }
    return (result);
}
*/



function validate(){
    var result = true;
    var e = document.getElementsByName("email")[0].value;

    var atindex = e.indexOf('@');
    var dotindex = e.lastIndexOf('.');
    if(atindex<1 || dotindex>=e.length-2 || dotindex-atindex<3){
        result = false;
        alert("email id is not entered in proper formate");
    }
    return result;
}


function confirmation_box(){
    var x = document.getElementById("sub");
    x = alert("Thanks for signing up, we acknowledge you by giving holyland reg no once we schedule the tour.");
}
$("#signUpForm").on('submit',function(){
    if($('#passwordRegister').val()!=$('#passwordConfirmRegister').val()){
        alert('Passwords do not match');
        return false;
    }
    return true;
 });



// Reset register details on close "x"
 $("#closeSignUpHeader").click(function(){
    $('#passwordConfirmRegister').val("");
    $('#passwordRegister').val("");
    $('#emailRegister').val("");
})
// Reset register details on close "close"
$("#closeSignUpFooter").click(function(){
    $('#passwordConfirmRegister').val("");
    $('#passwordRegister').val("");
    $('#emailRegister').val("");
})


// Reset login details on close "x"
$("#closeLogInHeader").click(function(){
    $('#emailLogIn').val("");
    $('#passwordLogIn').val("");
})
// Reset login details on close "close"
$("#closeLogInFooter").click(function(){
    $('#emailLogIn').val("");
    $('#passwordLogIn').val("");
})


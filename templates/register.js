/*
ZIQI ZHAO
I rewrite the login.js because it has a bug if I use the original structure. Although I can fix that bug, the code will become too long.
If I use the original one, it will occur a bug: after the Password and Confirm Password Match changes to green, if you change the password,
it will still show green and pass the test. That's because it does not have an I called 'after test.' So I changed some structure to
fix this bug.
*/
function openModal() {
    /* Note that you do NOT have to do a document.getElementById anywhere in this exercise. Use the elements below */
    var myUser = document.getElementById("user");
    var myInput = document.getElementById("psw");
    var confirmMyInput = document.getElementById("cpsw");
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");
    var match = document.getElementById("match");

    // When the user starts to type something inside the password field
    myInput.onkeyup = function() {
        //check after enter the password
        passIf();
    }
    /* TODO Question 1.3: Starts here */
    confirmMyInput.onkeyup = function() {
        //double check after enter the confirm password
        passIf();
    }
    //check the requirement
    function passIf (){

            /* TODO: Question 1.1: Starts here */
            var lowerCaseLetters = /[a-z]/g; // : Fill in the regular experssion for lowerCaseLetters
            var upperCaseLetters = /[A-Z]/g; // : Fill in the regular experssion for upperCaseLetters
            var numbers = /[0-9]/g; // : Fill in the regular experssion for digits
            var minLength = 8; // : Change the minimum length to what what it needs to be in the question
            /* TODO: Question 1.1: Ends here */


            /* TODO: Question 1.2:  Starts here */
             /*
             - So first read up on classList.
             - Perform a console.log(letter.classList) and check the array that you see. By default the first time, there should be just 1 element and it should be
             "invalid". "invalid" is a class that is present in login.css.
             - Below, there are a bunch of if blocks and else blocks.
             - Each if block means that some successful condition is satisfied for our password conditon. So the red cross need to be converted to a check mark.
             - Each else block stands for a failed condition, so the green check mark needs to be a red cross again.
             - All that you need to do is, in each of the blocks, fill in the correct classNames for the remove and the add methods.
             */

            // Validate lowercase letters
            if(myInput.value.match(lowerCaseLetters)) {
                letter.classList.remove("invalid");
                letter.classList.add("valid");
            } else {
                letter.classList.remove("valid");
                letter.classList.add("invalid");
            }

            // Validate capital letters
            if(myInput.value.match(upperCaseLetters)) {
                capital.classList.remove("invalid");
                capital.classList.add("valid");
            } else {
                capital.classList.remove("valid");
                capital.classList.add("invalid");
            }

            // Validate numbers
            if(myInput.value.match(numbers)) {
                number.classList.remove("invalid");
                number.classList.add("valid");
            } else {
                number.classList.remove("valid");
                number.classList.add("invalid");
            }

            // Validate length
            if(myInput.value.length >= minLength) {
                length.classList.remove("invalid");
                length.classList.add("valid");
            } else {
                length.classList.remove("valid");
                length.classList.add("invalid");
            }
            // Validate password and confirmPassword
            var passEqualsConfPass = (myInput.value == confirmMyInput.value); // TODO: Change this to the condition that needs to be checked so that the text entered in password equals the text in confirm password
            if(passEqualsConfPass) {
                match.classList.remove("invalid");
                match.classList.add("valid");
            } else {
                match.classList.remove("valid");
                match.classList.add("invalid");
            }

            //enable button after check requriement
            enableButton(letter, capital, number, length, match);
    }
    //check requirment
    function enableButton(letter, capital, number, length, match) {
        // TODO: Clear this function for students to implement
        var button = document.getElementById('my_submit_button');
        var condition = (letter.classList == "valid" &&
            capital.classList == "valid" &&
            number.classList == "valid" &&
            length.classList == "valid" &&
            match.classList == "valid"); // TODO: Replace false with the correct condition
        if(condition == true) {
                button.disabled = false;
        }
        else{
            button.disabled = true;
        }
    }
}

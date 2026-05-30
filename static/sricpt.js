document.addEventListener("DOMContentLoaded",function(){
    const form = document.querySelector("form");
    if (!form) return;

    const username = document.querySelector("input[name='username']");
    const password = document.querySelector("input[name='password']");
    const conf_password = document.querySelector("input[name='confirm_password']");

    //Validation
    function validate(field, condition, message){
        let error = field.parentElement.querySelector(".error-message");

        if (!condition){
            if (!error){
                error = document.createElement("p");
                error.classList.add("error-message");
                field.parentElement.appendChild(error);
            }

            error.textContent = message;
            field.classList.add("invalide-field");

            return false;
        }
        else {
            if (error) error.remove();
            field.classList.remove("invalide-field");
            return true;
        }
    }

    //Real time
    username.addEventListener("input", function(){
        validate(username, username.value.trim().length>=4,"Username must be at least 4 characters long.");
    });

    password.addEventListener("input", function(){
        validate(password, password.value.trim().length>=8,"Password must be longer than 8 characters long.");
    });

    conf_password.addEventListener("input", function(){
        validate(conf_password, conf_password.value== password.value,"Passwords must be identical.");
    });

    //Submit
    form.addEventListener("submit",function(event){
        const username_ok = validate(username, username.value.trim().length>=4,"Username must be at least 4 characters long.");
        const password_ok = validate(password, password.value.trim().length>=8,"Password must be longer than 8 characters long.");
        const conf_password_ok = validate(conf_password, conf_password.value== password.value,"Passwords must be identical.");

        if (!username_ok || !password_ok || !conf_password_ok){
            event.preventDefault();
            return;
        }
    })
})
// this function for hover the cliked event in dashboard
let list = document.querySelectorAll(".navigation li");

function activateLink(){
    list.forEach((item) => 
        item.classList.remove('hovered'));
        this.classList.add('hovered');
}

list.forEach((item) => 
    item.addEventListener("clicked",activateLink)    
)

//toggle bar button 

let toggle = document.querySelector('.toggle');
let navigation = document.querySelector('.navigation');
let main = document.querySelector('.main');

    toggle.onclick = function(){
        navigation.classList.toggle('active');
        main.classList.toggle('active');
    }

//progress bar 

let progressBar = document.querySelector(".progressBar");
let inp = document.getElementById("activeStocks");
let value = document.querySelector(".value");

value.textContent = inp.value + "%";
let percent = inp.value; 

progressBar.style.background = `conic-gradient(var(--blue) ${percent * 3.6}deg,#ededed 0deg)`
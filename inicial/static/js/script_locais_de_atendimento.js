const wrapper = document.querySelector(".wrapper"),
selectBtn = wrapper.querySelector(".select-btn"),
searchInp = wrapper.querySelector("input"),
options = wrapper.querySelector(".options");
 
//array of some UF.
let UF = ["AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"];

function addUF(selectedUF) {
    options.innerHTML = "";
    UF.forEach(uf => {
        // if selected UF and UF value is same, then add selected class.
        let isSelected = uf == selectedUF ? "selected" : "";
        // adding each UF inside <li> and inserting all li inside options tag
        let li = `<li onclick="updateName(this)" class="${isSelected}">${uf}</li>`;
        options.insertAdjacentHTML("beforeend", li);
    });
}
addUF();

function updateName(selectedLi) {
    searchInp.value = "";
    addUF(selectedLi.innerText);
    wrapper.classList.remove("active");
    selectBtn.firstElementChild.innerText = selectedLi.innerText;
}

searchInp.addEventListener("keyup", () => {
    let arr = []; // creating empty array.
    let searchedVal = searchInp.value.toLowerCase();
    // returning all UF from array which are start with user searched value.
    // and mapping returned UF with <li> and joining them.
    arr = UF.filter(data => {
        return data.toLowerCase().startsWith(searchedVal);
    }).map(data => `<li onclick="updateName(this)">${data}</li>`).join("");
    options.innerHTML = arr ? arr : `<p>UF não encontrada.</p>`;
});

selectBtn.addEventListener("click", () => {
    wrapper.classList.toggle("active");
});

var coll = document.getElementsByClassName("login_box");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content_account = this.nextElementSibling;
    if (content_account.style.display === "flex") {
      content_account.style.display = "none";
      this.style.borderRadius = "20px";
    } else {
      content_account.style.display = "flex";
      this.style.borderRadius = "20px 20px 0 0";
    }
  });
}

$(document).ready(function(){
   $("#btnPesquisar").click(function(){
    $("#top-bar1").toggle("fast");
    $("#top-bar2").hide("fast");
    $("#top-bar3").hide("fast");
    $("#fechar_aba").show("fast");
  });
  $("#locais_de_atendimento").click(function(){
    $("#top-bar2").toggle("fast");
    $("#top-bar1").hide();
    $("#top-bar3").hide();
    $("#fechar_aba").show("fast");
  });
  $("#outras_duvidas").click(function(){
    $("#top-bar3").toggle("fast");
    $("#top-bar1").hide();
    $("#top-bar2").hide();
    $("#fechar_aba").show("fast");
  });
  $("#fechar_aba").click(function(){
    $("#top-bar1").hide();
    $("#top-bar2").hide();
    $("#top-bar3").hide();
  });
  $(".voltar").click(function(){
    $("#top-bar1").show();
    $("#top-bar2").hide();
    $("#top-bar3").hide();
    $("#fechar_aba").show("fast");
  }); 
  $(".login_box").click(function(){
    $("#top-bar1").hide();
    $("#top-bar2").hide();
    $("#top-bar3").hide();
  }); 
});
$(window).scroll(function() {
    if ($(this).scrollTop() > 1){  
    $("#top-bar1").addClass("fixed");
    $("#top-bar2").addClass("fixed");
    $("#top-bar3").addClass("fixed");
    }
    else{
    $("#top-bar1").removeClass("fixed");
    $("#top-bar2").removeClass("fixed");
    $("#top-bar3").removeClass("fixed");
    }
});

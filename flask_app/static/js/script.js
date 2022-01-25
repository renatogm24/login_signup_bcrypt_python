
window.onload = function() {
  const element = document.querySelector(".messageSent");
  console.log(element);
  setTimeout(()=>{
    element.classList.add("hideMessage")
  },3000);
};
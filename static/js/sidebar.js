function w3_open() {
  document.getElementById("main").style.marginLeft = "25%";
  document.getElementById("mySidebar").style.width = "25%";
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("openNav").style.display = 'none';
}
function w3_close() {
  document.getElementById("main").style.marginLeft = "0%";
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("openNav").style.display = "inline-block";
}



function Validate() {
    var checked = 0;
    var bt = document.getElementById('btSubmit');
    //Reference the Table.
    var tblFruits = document.getElementById("roles");

    //Reference all the CheckBoxes in Table.
    var chks = tblFruits.getElementsByTagName("INPUT");

    //Loop and count the number of checked CheckBoxes.
    for (var i = 0; i < chks.length; i++) {
        if (chks[i].checked) {
            checked++;
        }
    }

    if (checked > 0) {
        //alert(checked + " CheckBoxe(s) are checked.");
        
        document.getElementById('count').innerHTML 
        = checked; 
        bt.disabled = false;
        return true;
    } else {
        //alert("Please select CheckBoxe(s).");
        document.getElementById('count').innerHTML 
        = checked;
        bt.disabled = true;
        return false;
    }
};

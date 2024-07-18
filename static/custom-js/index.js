document.addEventListener("DOMContentLoaded", function() {
    var editButtons = document.querySelectorAll("#buttn");
    var editButton = document.querySelectorAll(".btn");
    

    


  
    editButtons.forEach(function(button) {
      button.addEventListener("click", function() {
        var row = this.closest("tr");
  
        var itemId = row.querySelector("#id").value;
        console.log(itemId)
        var itemName = row.querySelector("#name").textContent; // Example, replace with your actual column class
        
        console.log(itemTitles)
        document.getElementById("item-id").value = itemId;
        document.getElementById("item-name").value = itemName;
        


  
        document.getElementById("myModal").style.display = "block";
      });
    });
  
    document.querySelector(".close").addEventListener("click", function() {
      document.getElementById("myModal").style.display = "none";
    });
  
    document.getElementById("save-btn").addEventListener("click", function() {
      // Save the edited data
      // You may want to update the item data in the database
      // Close the modal
      document.getElementById("myModal").style.display = "none";
    });


    editButton.forEach(function(button) {
        button.addEventListener("click", function() {
          var row = this.closest("tr");
    
          var itemId = row.querySelector("#id").value;
          var itemName = row.querySelector("#name").textContent; // Example, replace with your actual column class
          var gid = row.querySelector("#gid").textContent; 
          console.log(gid)
          var tab_id=row.getElementsByClassName("title-ids");
          var tab_title=row.getElementsByClassName("title-names");

          id=""
          title=""
        
          for (let i of tab_id){
            id+=i.textContent+","
          }
          for (let i of tab_title){
            title+=i.textContent+","
          }
          
          console.log(id)
          console.log(title)

    
          document.getElementById("itemid").value = itemId;
          document.getElementById("gitemid").value = gid;
          document.getElementById("titleid").value = id;
          document.getElementById("itemname").value = itemName;
          document.getElementById("titlenames").value=title;
          
          
    
          let modal=document.getElementById("myModal")

            modal.style.display = "block";
          
        });
      });
    
      document.querySelector(".close").addEventListener("click", function() {
        document.getElementById("myModal").style.display = "none";
      });
    
      document.getElementById("save-btn").addEventListener("click", function() {
        // Save the edited data
        // You may want to update the item data in the database
        // Close the modal
        document.getElementById("myModal").style.display = "none";
      });
  
  




      let alert=document.getElementById('alertMessage')
      setTimeout(function() {
        if (alert!=null){

          alert.style.display = 'none';
        }
      }, 2000);






























/**---------------------------------------------------------------------------------------------- */





  });
  
function submit_order(){
    
    console.log(myCart)
  fetch("/submit_order", {
          "method": "POST",
          "headers": {"Content-Type": "application/json"},
          "body": JSON.stringify({"cart" : (myCart),
          "total_price":2
          })
      }).then((response) => 
      console.log(response)
     )
  }
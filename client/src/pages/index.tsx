import React, { useState } from 'react';
import { Input, Card, Button } from 'antd';

export default function Home() {
  const [prodID, setProdID] = useState(''); // create a useState for setting the correct product 
  const [information, setInformation] = useState<any>(null) // create a useState for storing/setting the information on a product
  const handleLookup = async () => { // function that will handle what happens when the user clicks search for a product id
    if (!prodID){ // if the user does not give a product id then give an alert
      alert('Product ID Not Given. Please enter a Product ID.')
      return;
    }
    else{
      try{
        const query = await fetch(`http://localhost:5001/products/${prodID}`); // fetch the URL with the product id that the user inputs
        const json = await query.json(); // create the json
        if (query.ok){ // if the fetch for the URL was valid then we can set the information
          setInformation(json);
        }
        else{
          console.error("Not Found Error") // if the fetch for the URL was not valid, then we throw an error
          alert("404 Not Found")
        }
      }
      catch(error){
        console.error('Server Error', error); // Throw an error for a server error 
        alert('There is a Server Error');

      }

    }
  }
  return <>
  <Input  // gets input from user and sets the prodict to be the id that the user inputs
    placeholder="Enter Product ID"
    value={prodID}
    onChange={(e) => setProdID(e.target.value)}
  />
  <br></br>
  <Button onClick={handleLookup}  // button that calls handleLookup which will search for URL of product
        style={{
          fontSize: '16px',
          backgroundColor: 'black',
          color: 'white',
        }}
        >Search</Button> 
  {information && (  // checks to make sure the information is set and if it is, we can list out all the necessary information that is stored for that specific product id
  <div style={{textAlign:"center"}}>
      <h1 style={{textAlign:"center"}}>Information on the Product!</h1>
    <p style={{textAlign: "center", display: "inline", fontSize: "25px"}}><b>Name: </b></p> <p style={{display: "inline", alignContent: "center", justifyContent: "center", textAlign: "center", fontSize: "22px"}}>{information.product_id.name}</p>
    <br></br>
    <p style={{textAlign: "center", display: "inline", fontSize: "25px"}}><b>Price: </b></p> <p style={{display: "inline", alignContent: "center", justifyContent: "center", textAlign: "center", fontSize: "22px"}}>{information.product_id.price}</p>
    <br></br>
    <p style={{textAlign: "center", display: "inline", fontSize: "25px"}}><b>Description: </b></p> <p style={{display: "inline", alignContent: "center", justifyContent: "center", textAlign: "center", fontSize: "22px"}}>{information.product_id.description}</p>
<br></br>
    <p style={{textAlign: "center", display: "inline", fontSize: "25px"}}><b>ID: </b></p> <p style={{display: "inline", alignContent: "center", justifyContent: "center", textAlign: "center", fontSize: "22px"}}>{information.product_id.id}</p>
<br></br>
    <p style={{textAlign: "center", display: "inline", fontSize: "25px"}}><b>Created At: </b></p> <p style={{display: "inline", alignContent: "center", justifyContent: "center", textAlign: "center", fontSize: "22px"}}>{information.product_id.created_at}</p>

  </div>
)}
</>
}



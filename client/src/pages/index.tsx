import React, { useState } from 'react';
import { Input, Card, Button } from 'antd';

export default function Home() {
  const [prodID, setProdID] = useState('');
  const [information, setInformation] = useState<any>(null)
  const handleLookup = async () => {
    if (!prodID){
      alert('Product ID Not Given. Please enter a Product ID.')
      return;
    }
    else{
      try{
        console.log("here")
        const query = await fetch(`http://localhost:5001/products/${prodID}`);
        const json = await query.json();
        if (query.ok){
          setInformation(json);
        }
        else{
          console.error("Not Found Error")
          alert("404 Not Found")
        }
      }
      catch(error){
        console.error('Server Error', error);
        alert('There is a Server Error');

      }

    }
  }
  return <>
  <Input
    placeholder="Enter Product ID"
    value={prodID}
    onChange={(e) => setProdID(e.target.value)}
  />
  <br></br>
  <Button onClick={handleLookup}
        style={{
          fontSize: '16px',
          backgroundColor: 'black',
          color: 'white',
        }}
        >Search</Button>
  {information && (
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



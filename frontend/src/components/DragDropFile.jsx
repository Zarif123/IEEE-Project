import React, { useState, useEffect } from "react";
import "./DragDropFile.css";
// drag drop file component
function DragDropFile() {
    // drag state
    const [dragActive, setDragActive] = React.useState(false);
    // ref
    const inputRef = React.useRef(null);
    const [foodText, setFoodText] = useState("Go ahead and upload your food image!");
    //handle uploaded image
    const [ingredients, setIngredients] = React.useState([]);
    const [foodName, setFoodName] = React.useState("");
    const handleUpload = function(image) {
      if (! (image && image['type'].split('/')[0] === 'image')){
        alert("Please upload an image first!");
      }
      else{
          // Using fetch to fetch the api from 
          // flask server it will be redirected to proxy
          var fileReader = new FileReader();
          fileReader.onload = function(fileLoadedEvent) {
            var srcData = fileLoadedEvent.target.result;

            var newImage = document.createElement('img');
            newImage.src = srcData;
            document.getElementById("imgShow").innerHTML = newImage.outerHTML;
            var imageString = newImage.src.split(",")[1];
            let imagePackage = {'img': imageString};
            fetch('/imgResponse', {
              method: 'Post',
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(imagePackage)
            }).then((res) =>
              res.json().then((data) => {
                console.log(data);
                setIngredients(data["ingredients"]);
                setFoodName(data["foodName"]);
                setFoodText("You can check a different picture!");
              })
            );
          }
          fileReader.readAsDataURL(image);
          console.log(image);
          
      };
    }

    // handle drag events
    const handleDrag = function(e) {
      e.preventDefault();
      e.stopPropagation();
      if (e.type === "dragenter" || e.type === "dragover") {
        setDragActive(true);
      } else if (e.type === "dragleave") {
        setDragActive(false);
      }
    };
    
    // triggers when file is dropped
    const handleDrop = function(e) {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleUpload(e.dataTransfer.files[0]);
        
      }
    };
    
    // triggers when file is selected with click
    const handleChange = function(e) {
      e.preventDefault();
      if (e.target.files && e.target.files[0]) {
        handleUpload(e.target.files[0]);
      }
    };
    
  // triggers the input when the button is clicked
    const onButtonClick = () => {
      inputRef.current.click();
    };
    
    return (
      
      <div className="content">
        <h3 className="basic-text">{foodText}</h3>
        {
          <form id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
            <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} />
            { dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div> }
            <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : "" }>
                <button className="upload-button" onClick={onButtonClick}>Upload your image!</button>
            </label>
          </form>
        }
        
        <div className="totalContainer">
          <div className="imgShow" id="imgShow"></div>
          <div className="foodBox">
            {
              (ingredients.length !== 0) && 
              <h4 className="foodName">
                You're eating {foodName}!
              </h4>
            }
            {
              (ingredients.length !== 0) && 
              <h4 className="foodName">
                The ingredients are:
              </h4>
            }
            <div className="ingBox">
              {
                
                ingredients.map((ingredient) => {
                    return <p className="ingredient">
                      {ingredient}
                    </p>
                })
              }
            </div>
          </div>
        </div>
      </div>
    );
  };
  export default DragDropFile;
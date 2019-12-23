import React, { Component } from 'react'
import {Container} from 'react-bootstrap';
import { FaRegStar } from 'react-icons/fa';
import { FaStar} from 'react-icons/fa';





const stars =(no) => {
    let i =0;
    var stararray=[];
    
    for (  i =0 ; i <  no ; i++){
        stararray.push(<FaStar size={25}/>)
    }
    for ( ; i < 5 ; i++){
        stararray.push(<FaRegStar size={25}/>)
    }
    return stararray;
};

const Assg = (e) => {
    const { no , prob_name} = e;
    let a = e.no ? e.no : 69;
    let b = prob_name === "" ? prob_name : "Placeholder Question No";
    return (
      <div
        style={{
          paddingTop: "0.5em"
        }}
      >
        <Container
          style={{
            marginLeft: "0.5em",

            // boxShadow: "-1px 0px 2px #d4d2d2",
            // borderRight: "1px solid #d4d2d2",
            
            paddingLeft: "0px",
            width: "70%",
            paddingRight: "0px",
            marginTop: "5px",
            display: "flex",
            flexDirection: "horizontal",
            backgroundColor: "#ffffff",
            height: "7rem",
            justifyContent: "true",
            alignItems: "center",
            fontSize: "2.4vw"
          }}
        >
          <div
            style={{
              padding: "10px",
              marginLeft: "0px"
            }}
          >
            <h1
              style={{
                padding: "5px",
                paddingTop:"1.3em",

                borderBottom: "2px solid #dee0df"
              }}
            >
              # Assignment {a}{" "}
            </h1>
            <div>{b}</div>
          </div>

          <div
            style={{
              backgroundColor: "#ffffff"
            }}
          >
            <div
              style={{
                position: "relative",
                left: "3em",
                width: "100%",
                display: "flex",
                flexDirection: "horizontal"
              }}
            >
              <strong>Difficulty</strong>
              {stars(4)}
            </div>
          </div>
        </Container>
      </div>
    );
}

export default Assg;
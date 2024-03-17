import React, { useState } from 'react';
import '../App.css';
import './item.css';
import { SERVER_ADDRESS, NFT_COST } from '../config'
import ValidityChecker from "../components/BTCvalidator";
import CopyToClipboard from '../components/CopyToClipboard';
import { useLocation } from "react-router-dom";


function Item() {
  const location = useLocation();
  // const imageid = location.state.imageId
  console.log(location.state.imageId)
  const [address, setAddress] = useState('');
  const [transactionNumber, setTransactionNumber] = useState('');
  // const [clickedImageId, setClickedImageId] = useState(null);
  const [isDepositAddress, setIsDepositAddress] = useState(false);


  // const handleBlur = () => {
  // console.log('Checking address ' + address);
  //     ValidityChecker(address)

  // };


  const handleBuyClick = async (imageId) => {
    // console.log(transactionNumber + ' ' + imageId + ' ' + address)
    fetch(SERVER_ADDRESS + '/get_deposit_address', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "data": address, "id": imageId })
    })
      .then(response => response.json())
      .then(data => {
        setTransactionNumber(data.transactionNumber);
        setIsDepositAddress(true);
      })
      .catch(error => console.error(error));
  };

  return (

    <div className='item section__padding'>
      <div className="item-content">
        <div className="item-content-title">
          <h1>Item {location.state.imageId}</h1>

          <div className="item-image">
            <img src={`${SERVER_ADDRESS}/images/${location.state.imageId}.png`} />
          </div>

          <p>Buy <span> {NFT_COST} BTC</span> 1 of 1 available</p>
        </div>
        <div className="item-content-creator">
          <div><p>Creater</p></div>

          <label htmlFor="address">Enter BTC address to receive Ordinal: </label>
          <input
            id="address"
            type="text"
            value={address}
            onChange={e => setAddress(e.target.value)}
            maxLength="62"
            width="75%"
          // onBlur={handleBlur}
          />

        </div>
        <div className="item-content-detail">
          <p>Anothr nice Ordinal Inscription</p>
        </div>
        <div className="item-content-buy">
          {isDepositAddress ? (
            <CopyToClipboard text={transactionNumber} />
          ) : (
            <button
              className="primary-btn"
              onClick={() => handleBuyClick(location.state.imageId)}
            >
              "Get deposit address!"
            </button>
          )}
          <button className="secondary-btn">Refresh Transactions</button>
        </div>
      </div>

    </div>
  );
}

export default Item;
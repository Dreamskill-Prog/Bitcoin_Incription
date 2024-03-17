import React, { useState, useEffect } from 'react';
import '../App.css';
import { SERVER_ADDRESS, NFT_COST } from '../config'
import { Link } from 'react-router-dom';

function Collection() {
    const [images, setImages] = useState([]);

    useEffect(() => {
        console.log(SERVER_ADDRESS + '/images')
        fetch(SERVER_ADDRESS + '/images')
            .then(response => response.json())
            .then(data => {
                setImages(data);
                console.log(data)
            })
            .catch(error => console.error(error));
    }, []);

    return (
        <div className="Collection">
            <h1>Ordinary Inscriptions</h1>
            <br />
            <ul>
                <li> Enter the BTC wallet address you wish to receive your ordinal at.</li>
                <li> Select the Ordinal you would like to aquire.</li>
                <li> You will be given a unique deposit-address. </li>
                <li> Deposit {NFT_COST} BTC into the deposit-address to receive your Ordinal!</li>
                <li> This will take minimum of two blocks - 1 to confirm the deposit, 1 to send the Ordinal Inscription.</li>
                <li> If no deposit has been broadcast within 3 blocks, your order will be cancelled.</li>
            </ul>

            <br />
            <label htmlFor="address">Pick your Ordinal to inscribe from the Collection: </label>
            <div className="gallery">
                {images.map(image => (
                    <div key={image.id} className="ImageContainer">
                        <img
                            src={`${SERVER_ADDRESS}/images/${image.id}.png`}
                            alt={`Ordinal ${image.id}`}
                            className={image.available ? 'img-available' : 'img-unavailable'}
                        />
                        <br />
                        <Link to={{ pathname: `/Ordinal/${image.id}` }} state={{ imageId: image.id }}  >
                            <button
                                className={image.available ? 'button-available' : 'button-unavailable'}
                                disabled={!image.available}
                            >
                                {image.available ? "Claim Inscription!" : "Unavailable"}
                            </button>
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Collection;
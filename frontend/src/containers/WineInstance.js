import React from 'react'
import axios from "axios";
import { useState, useEffect } from 'react';
import Button from 'react-bootstrap/esm/Button'
import Row from 'react-bootstrap/esm/Row'
import Col from 'react-bootstrap/esm/Col'
import { useParams } from 'react-router-dom';
import Container from 'react-bootstrap/esm/Container';
import VineyardCard from '../components/VineyardCard';
import RegionCard from '../components/RegionCard';


const WineInstance = () => {
    let { id } = useParams();
    const [name, setName] = useState('');
    const [country, setCountry] = useState('');
    const [region, setRegion] = useState('');
    const [type, setType] = useState('');
    const [winery, setWinery] = useState('');
    const [rating, setRating] = useState(0);
    const [reviews, setReviews] = useState(0);
    const [image, setImage] = useState('');
    const [reddit, setReddit] = useState([]);
    const [vineyards, setVineyards] = useState([]);
    const [regions, setRegions] = useState([]);

    useEffect(() => {
        let mounted = true;
        axios.get(`https://api.wineworld.me/wines/${id}`)
            .then(response => {
                if (mounted) {
                    setName(response.data['name']);
                    setCountry(response.data['country']);
                    setRegion(response.data['region']);
                    setType(response.data['type']);
                    setWinery(response.data['winery']);
                    setRating(response.data['rating']);
                    setReviews(response.data['reviews']);
                    setImage(response.data['image']);
                    setReddit(response.data['redditPosts']);
                    setVineyards(response.data.related['vineyards']);
                    setRegions(response.data.related['regions']);
                }
            })
            .catch(errRes => {
                console.error(errRes);
            });
        return () => mounted = false;
    }, [])

    return (
        <div>
            <Row>
                <Col>
                    <img src={image} class="img-fluid" alt="..."></img>
                    <h3>{name}</h3>
                    <h5 class="text-muted">{type} Wine</h5>
                </Col>
                <Col>
                    <div className='p-5'>
                        <p align="left">
                            Country: {country}
                            <br />
                            Region: {region}
                            <br />
                            Winery: {winery}
                            <br />
                            Rating: {rating}
                            <br />
                            Reviews: {reviews}
                        </p>
                    </div>
                </Col>
            </Row>
            <Row md={10} className="p-4 g-4">
                <h5 align="left">Related Vineyards</h5>
                {
                    vineyards.map((vineyard) => {
                        return (
                            <Col>
                                <VineyardCard vineyard={vineyard} />
                            </Col>

                        )
                    })
                }
            </Row>
            <Row md={10} className="p-4 g-4">
                <Col>
                    <h5 align="left">Related Regions</h5>
                    {
                        regions.map((region) => {
                            return (
                                <Col>
                                    <RegionCard region={region} />
                                </Col>

                            )
                        })
                    }
                </Col>

            </Row>
            {/* <Col>
                <iframe id={"reddit-embed"} src={`${reddit_link}?ref_source=embed&amp;ref=share&amp;embed=true`} sandbox={"allow-scripts allow-same-origin allow-popups"} style={{ border: "none" }} height={"249"} width={"640"} scrolling={"no"}></iframe>
            </Col> */}
            <Row>
                {
                    reddit.map((reddit_link) => {
                        return (
                            <Col>
                                <iframe id={"reddit-embed"} src={`${reddit_link}?ref_source=embed&amp;ref=share&amp;embed=true`} sandbox={"allow-scripts allow-same-origin allow-popups"} style={{ border: "none" }} height={"249"} width={"640"} scrolling={"no"}></iframe>
                            </Col>

                        )
                    })
                }
            </Row>
        </div>
    )
}
export default WineInstance

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import { useLocation } from 'react-router-dom';
import WineCard from '../components/WineCard';
import Spinner from 'react-bootstrap/Spinner';

const WineSearch = () => {
    const [wines, setWines] = useState([]);
    const [wineLoaded, setWineLoaded] = useState(false);
    const location = useLocation();
    const query = location.pathname.split("/Search/").at(-1);
    const words = query.split('%20');
    const searchQuery = words.join(" ");

    useEffect(() => {
        async function searchWines() {
            const response = await axios.get('https://api.wineworld.me/wines', {
                params: {
                    name: searchQuery,
                },
            });
            setWines(response.data.list);
            setWineLoaded(true);
        }

        searchWines();
    }, [searchQuery])

    return (
        <Container>
            <h1> Wine Search Results</h1>
            <p style={{opacity: 0.65}} hidden = {wines.length > 0}>No wines seem to match your search</p>
            <Row md={4} className="d-flex g-4 p-4 justify-content-left">
                {wineLoaded ? (
                    wines.map(wine => (
                    <Col>
                        <WineCard wine={wine} regex={searchQuery} />
                    </Col>
                    ))) : (
                    <Spinner animation="border" role="status"></Spinner>
                )
                }
            </Row>
        </Container>
    )
}

export default WineSearch
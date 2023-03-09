import React from 'react';
import Card from 'react-bootstrap/Card';
// Import Button from "react-bootstrap/esm/Button";
import { Link } from 'react-router-dom';
import { handleRegionImageError } from '../util/handleImageError';

const RegionCard = props => {
    const {
        id,
        name,
        country,
        rating,
        reviews,
        // Tags,
        tripTypes,
        image,
        // ImageHeight,
        // imageWidth,
        // url,
    } = props.region;

    return (
        <Card border="dark" style={{ height: '30rem', width: '18rem' }}>
            <Card.Img
                variant="top"
                src={image.url}
                style={{ height: '50%', width: '100%', objectFit: 'cover' }}
                onError={handleRegionImageError}
            />
            <Card.Body>
                <Card.Title> {name} </Card.Title>
                <Card.Subtitle> {country} </Card.Subtitle>
                <Card.Text>
                    <small>
                        Rating: {rating}
                        <br />
                        Review Count: {reviews}
                        <br />
                        Trip Type: {tripTypes.join(', ')}
                        {/* <br />
                        Tags: {tags.join(", ")} */}
                    </small>
                </Card.Text>
            </Card.Body>
            <div class="card-footer">
                <Link to={`/Regions/${id}`} class="btn btn-secondary stretched-link">
                    Explore Region
                </Link>
            </div>
        </Card>
    );
};

export default RegionCard;

import './Card.css';
import React from 'react';
import { Link } from 'react-router-dom';

export default ({ title, footerText, linkUrl, textLink, ...props }) => {
    return (
        <div className='Card'>
            { title && 
                <>
                    <h2 className='CardTitle my-2'>{title}</h2>
                    <hr />
                </> 
            }
            
            <div className='CardContent'>{props.children}</div>
            { linkUrl && 
                <div className='mt-4 CardFooter'>
                    {footerText} &nbsp; 
                    <Link className='CardLink' to={linkUrl}>
                        {textLink}
                    </Link>
                </div>
            }
            
        </div>
    )
}
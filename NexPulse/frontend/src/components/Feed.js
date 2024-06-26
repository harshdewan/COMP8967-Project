import React from 'react';
import './Feed.css'; // Import CSS for styling
import tulip from "./tulip.jpeg"

const Feed = () => {
    return (
        <div className="main-content">
            <header>
                <nav>
                    <a href="#" className="active">Home</a>
                    <a href="#">Following</a>
                    <a href="#">Explore</a>
                </nav>
            </header>
            <section className="posts">
                <article className="post">
                    <div className="post-header">
                        <img src={tulip}  />
                        <div>
                            <h2>Helena</h2>
                            <p>in Group name • 3 min ago</p>
                        </div>
                    </div>
                    <img className="postt" src={tulip} />
                    <p>Post description</p>
                    <div className="post-actions">
                        <span>21 likes</span>
                        <span>4 comments</span>
                    </div>
                </article>
                <article className="post">
                    <div className="post-header">
                        <img src={tulip} />
                        <div>
                            <h2>Charles</h2>
                            <p>in Group name • 2 hrs ago</p>
                        </div>
                    </div>
                    <p>Body text for a post. Since it’s a social app, sometimes it’s a hot take, and sometimes it’s a question.</p>
                    <div className="post-actions">
                        <span>6 likes</span>
                        <span>18 comments</span>
                    </div>
                </article>
            </section>
        </div>
    );
};

export default Feed;

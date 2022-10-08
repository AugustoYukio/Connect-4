import React from "react";
import "./Game.css";

export default () => {
    return (
        <div className="Game">
            <div className="container">
                <div className="text-center" id="loading">
                    <h1 className="display-4">Loading...</h1>
                </div>
                <div className="row">
                    <div className="col">
                        <div className="canvasContainer" id="game"></div>
                    </div>
                </div>
                <div className="row">
                    <div className="col">
                        <img
                            id="redturnIn"
                            src={require("../../res/img/bestchipred.png")}
                            className="chipIndicator img-fluid float-left"
                        />
                        <h5>
                            <span id="redVic" className="badge badge-danger chipIndicator">0</span>
                        </h5>
                    </div>
                    <div className="col mx-auto my-auto text-center">
                        <h6 id="game-status"></h6>
                        <div id="copyBox" className="input-group mb-3">
                            <input
                                id="hostLink"
                                type="text"
                                className="form-control"
                                value=""
                                onFocus={e => e.target.select()}
                                //onBlur="window.getSelection().removeAllRanges();"
                                aria-label="host link"
                                style={{ backgroundColor: 'white' }}
                                aria-describedby="basic-addon2"
                                readOnly
                            />
                            <div className="input-group-append">
                                <button
                                    id="copyButton"
                                    className="btn btn-outline-primary"
                                    type="button"
                                    data-container="body"
                                    data-toggle="popover"
                                    data-placement="bottom"
                                    data-trigger="focus"
                                    data-delay='{"hide": 1000}'
                                    data-content="Copied!"
                                >
                                    Copy
                                </button>
                            </div>
                        </div>
                        <button
                            type="button"
                            className="btn btn-primary big-screen-button"
                            id="resetButton"
                        //onClick={''}
                        >
                            Menu
                        </button>
                        <div className="col">
                            <button
                                type="button"
                                className="btn btn-danger big-screen-button"
                                id="playAgainButton"
                            >
                                Play Again
                            </button>
                        </div>
                    </div>
                    <div className="col">
                        <img
                            id="blueturnIn"
                            src={require("../../res/img/bestchipblue.png")}
                            className="chipIndicator img-fluid float-right"
                        />
                        <h5>
                            <span
                                id="blueVic"
                                className="badge badge-primary chipIndicator float-right"
                            >0</span
                            >
                        </h5>
                    </div>
                </div>
            </div>

            <div
                className="modal fade"
                id="gamemodeSelector"
                data-keyboard="false"
                data-backdrop="static"
            >
                <div style={{ textAlign: 'center' }}>

                    <div
                        className="modal-dialog"
                        role="document"
                        style={{ display: 'inline-block' }}
                    >
                        <div className="modal-content">
                            <div className="row mx-auto">
                                <h4>Connect 4</h4>
                            </div>
                            <div className="modal-body mx-auto" style={{ textAlign: 'center' }}>
                                <div id="gamemodeSelectorButtons" role="group">
                                    <button type="button" className="btn btn-primary" id="single">
                                        Single Player
                                    </button>
                                    <button type="button" className="btn btn-primary" id="local">
                                        Local Multiplayer
                                    </button>
                                    <button type="button" className="btn btn-primary" id="host">
                                        Online Multiplayer
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
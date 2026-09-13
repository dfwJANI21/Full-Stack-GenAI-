function LoadingStatus({theme}){
    return <div className="loading-container">
        <h2>Generating Your {theme} Story</h2>

        <div className="loading-animation">

        </div>
        <p className="loading-info">Please wait while we generate story</p>

    </div>

}

export default LoadingStatus; 

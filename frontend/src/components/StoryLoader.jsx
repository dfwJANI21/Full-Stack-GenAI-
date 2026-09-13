import {useState,useEffect} from 'react';

import {useParam,useNavigate} from "react" 
import axios from 'axios';
import LoadingStatus from "./LoadingStatus.jsx"
const API_BASE_URL = "/api"

function StoryLoader(){
    const {id} = useParam();
    const navigate = useNavigate();
    const [story,setStory] = useState(null);
    const[loading,setLoading] = useState(null);
    const[error,setError] = useState(null);
    useEffect(()=>{
        loadStory(id)
    },[id])
    const loadStory = async (storyId)=>{
        setLoading(true)
        setError(null)
        
        try {
            const response = await axios.get('${API_BASE_URL}/stories/${storyId}/comlete')
            setStory(response.data)
            setLoading(false)
        } catch (err){
            if (err.response?.status === 404) {
                setError("Story is not found")
            } else {
                setError("Failed to load stroy")

            }
        } finally{
            setLoading(false)
        }
        
        
   
    }
    const createNewStory = ()=> {
            navigate("/")
    }
    if (loading) {
        return <LoadingStatus theme={"story"}/>
    }
    if (error){
        return <div className="stroy-loader">
            <div className="error-message">
                <h2>Story Not Found</h2>
                <p>{error}</p>
                <button onClick={createNewStory}>Go to Story Generator</button>
            </div>
        </div>
    }
    if (story){
        return <div className="story-loader">

        </div>
    }

}
export default StoryLoader;
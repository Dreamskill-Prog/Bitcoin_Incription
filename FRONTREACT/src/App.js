import './App.css';
// import {Footer} from './components'
//Add more pages here
// import { Collection } from './pages'
import { Routes, Route } from "react-router-dom";
// import { Collection } from "./pages/Collection"
import Collection from './pages/Collection';
import Item from './pages/Item';

function App() {

  return (
    <div>
      {/* <Navbar /> */}
          <Routes>
            <Route path=":item/:id" element={<Item />} />
            <Route path="/" element={<Collection />} />
          </Routes>
      {/* <Footer /> */}
    </div>
  );
}

export default App;

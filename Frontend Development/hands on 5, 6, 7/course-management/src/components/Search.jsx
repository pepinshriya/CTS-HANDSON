import React from 'react'
import { useState } from 'react'

const Search = ({handleChange}) => {
 const [searchItem, setSearchItem] = useState("");
  return (
    <div>
      <input
            type="text"
            placeholder="Search by name"
            value={searchItem}
            onChange={(e) => {
                setSearchItem(e.target.value)
                handleChange(e.target.value)
            }}
            />
    </div>
  )
}

export default Search

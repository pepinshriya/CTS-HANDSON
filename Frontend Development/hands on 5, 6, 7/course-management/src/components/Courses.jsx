import { useState } from 'react'
import { courses } from '../../public/data.js'
import CourseCard from './CourseCard'
import Search from './Search.jsx'

const Courses = () => {
  const [filteredCourses, setFilteredCourses] = useState(courses)

  const handleChange = (searchItem) => {
    const reduced = courses.filter((course) =>
      course.name.toLowerCase().includes(searchItem.toLowerCase()),
    )
    setFilteredCourses(reduced)
  }

  return (
    <>
      <Search handleChange={handleChange} />

      {filteredCourses.length > 0 ? (
        filteredCourses.map((course) => (
          <CourseCard key={course.id} course={course} />
        ))
      ) : (
        <p>No courses found.</p>
      )}
    </>
  )
}

export default Courses

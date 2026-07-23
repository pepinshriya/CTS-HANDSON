// ==============================
// TASK 1
// ==============================

// Create and switch to database
use("college_nosql");

// Create collection
db.createCollection("feedback");

// Insert the 10 feedback documents
db.feedback.insertMany([
  {
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching. Would recommend.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments: [
      { filename: "notes.pdf", size_kb: 240 }
    ]
  },
  {
    student_id: 2,
    course_code: "CS101",
    semester: "2022-EVEN",
    rating: 4,
    comments: "Good course with practical sessions.",
    tags: ["interactive", "practical", "informative"],
    submitted_at: ISODate("2023-04-15T09:20:00Z"),
    attachments: [
      { filename: "assignment.pdf", size_kb: 180 }
    ]
  },
  {
    student_id: 3,
    course_code: "CS101",
    semester: "2023-ODD",
    rating: 3,
    comments: "Course was okay but assignments were difficult.",
    tags: ["challenging", "assignments", "average"],
    submitted_at: ISODate("2023-11-28T11:10:00Z"),
    attachments: []
  },
  {
    student_id: 4,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 5,
    comments: "Loved the hands-on programming exercises.",
    tags: ["coding", "fun", "well-paced"],
    submitted_at: ISODate("2022-12-01T14:30:00Z"),
    attachments: [
      { filename: "project.zip", size_kb: 520 }
    ]
  },
  {
    student_id: 5,
    course_code: "CS102",
    semester: "2023-EVEN",
    rating: 2,
    comments: "Too much theory and less practical work.",
    tags: ["theory", "boring", "needs-improvement"],
    submitted_at: ISODate("2024-05-02T15:40:00Z"),
    attachments: []
  },
  {
    student_id: 6,
    course_code: "CS201",
    semester: "2023-ODD",
    rating: 4,
    comments: "Interesting subject with real-world examples.",
    tags: ["interesting", "examples", "clear"],
    submitted_at: ISODate("2023-11-20T13:25:00Z"),
    attachments: [
      { filename: "feedback.docx", size_kb: 95 }
    ]
  },
  {
    student_id: 7,
    course_code: "CS202",
    semester: "2024-EVEN",
    rating: 1,
    comments: "Teaching pace was too fast.",
    tags: ["fast", "confusing", "needs-support"],
    submitted_at: ISODate("2024-04-18T16:00:00Z"),
    attachments: []
  },
  {
    student_id: 8,
    course_code: "CS203",
    semester: "2024-ODD",
    rating: 5,
    comments: "Best course this semester.",
    tags: ["excellent", "organized", "engaging"],
    submitted_at: ISODate("2024-11-22T12:45:00Z"),
    attachments: [
      { filename: "certificate.pdf", size_kb: 150 }
    ]
  },
  {
    student_id: 9,
    course_code: "CS204",
    semester: "2023-EVEN",
    rating: 3,
    comments: "Content was useful but could be updated.",
    tags: ["useful", "outdated", "average"],
    submitted_at: ISODate("2024-05-10T08:30:00Z"),
    attachments: []
  },
  {
    student_id: 10,
    course_code: "CS205",
    semester: "2024-ODD",
    rating: 4,
    comments: "Instructor explained concepts clearly.",
    tags: ["clear", "supportive", "interactive"],
    submitted_at: ISODate("2024-11-30T17:20:00Z"),
    attachments: [
      { filename: "summary.pdf", size_kb: 210 }
    ]
  }
]);

// Insert one document WITHOUT attachments

db.feedback.insertOne({
  student_id: 11,
  course_code: "CS103",
  semester: "2024-EVEN",
  rating: 4,
  comments: "Well-organized course with engaging lectures.",
  tags: ["organized", "interactive", "informative"],
  submitted_at: ISODate("2024-12-05T10:30:00Z")
});

// Verify insert

db.feedback.countDocuments();


// ==============================
// TASK 2 - CRUD
// ==============================

// 65
// Find all rating 5

db.feedback.find({
    rating:5
});

// 66
// CS101 with challenging tag

db.feedback.find({
    course_code:"CS101",
    tags:"challenging"
});

// 67
// Projection

db.feedback.find(
{},
{
    student_id:1,
    course_code:1,
    rating:1,
    _id:0
}
);

// 68
// Add needs_review

db.feedback.updateMany(
{
    rating:{
        $lt:3
    }
},
{
    $set:{
        needs_review:true
    }
}
);

// 69
// Push reviewed tag

db.feedback.updateMany(
{
    needs_review:true
},
{
    $push:{
        tags:"reviewed"
    }
}
);

// 70
// Delete semester

db.feedback.deleteMany({
    semester:"2021-EVEN"
});


// ==============================
// TASK 3 - Aggregation
// ==============================

// 71
// Average rating

db.feedback.aggregate([
{
    $match:{
        semester:"2022-ODD"
    }
},
{
    $group:{
        _id:"$course_code",
        avg_rating:{
            $avg:"$rating"
        },
        total_feedback:{
            $sum:1
        }
    }
},
{
    $sort:{
        avg_rating:-1
    }
}
]);


// 72
// Rename and round

db.feedback.aggregate([
{
    $match:{
        semester:"2022-ODD"
    }
},
{
    $group:{
        _id:"$course_code",
        avg_rating:{
            $avg:"$rating"
        },
        total_feedback:{
            $sum:1
        }
    }
},
{
    $project:{
        _id:0,
        course_code:"$_id",
        average_rating:{
            $round:["$avg_rating",1]
        },
        total_feedback:1
    }
},
{
    $sort:{
        average_rating:-1
    }
}
]);


// 73
// Tag frequency leaderboard

db.feedback.aggregate([
{
    $unwind:"$tags"
},
{
    $group:{
        _id:"$tags",
        count:{
            $sum:1
        }
    }
},
{
    $sort:{
        count:-1
    }
}
]);


// 74
// Create Index

db.feedback.createIndex({
    course_code:1
});

// Verify Index Usage

db.feedback.find({
    course_code:"CS101"
}).explain("executionStats");
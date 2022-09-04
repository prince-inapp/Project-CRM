from flask import Blueprint, render_template, request,  jsonify, url_for, redirect

from website import views
from . import db
from .models import Category, Batches, CourseEnrollment, Courses, Enquiries, Users, Qualifications, ActivityLog, Instructor
import json
#from sqlalchemy import func, Date
from datetime import date
from flask_login import login_user, login_required, logout_user, current_user

userviews = Blueprint('userviews', __name__)

userEnquiries = []
ROWS_PER_PAGE = 5
#enquiry
@userviews.route('/enquiries', methods=['GET', 'POST'])
def userEnquiries():
    if request.method == 'POST':
        userEnquiryId = request.form.get('enquiryId')
        print(userEnquiryId)
        userEnquiryUserId = request.form.get('enquiryUserId')
        userEnquiryCourseId = request.form.get('enquiryCourseId')
        userEnquiryStatus = bool(request.form.get('enquiryStatus'))
        userEnquiryDescription = request.form.get('enquiryDescription')
        print(userEnquiryId, userEnquiryUserId, userEnquiryCourseId, userEnquiryDescription, userEnquiryStatus)
        new_enquiry = Enquiries(enquiryId=userEnquiryId, enquiryUserId=userEnquiryUserId, enquiryCourseId=userEnquiryCourseId, enquiryDescription=userEnquiryDescription)
        db.session.add(new_enquiry)
        db.session.commit()
    user=current_user
    #print(userEnquiryId, userEnquiryUserId, userEnquiryCourseId, userEnquiryDescription, userEnquiryStatus)
    userEnquiries=Enquiries.query.filter_by(enquiryUserId=user.userId)
    courses = Courses.query.with_entities(Courses.courseId, Courses.courseName).distinct().all()
    #users = Users.query.with_entities(Users.userId).distinct().all()
    userEnquiryStatus = Enquiries.query.with_entities(Enquiries.enquiryStatus).distinct().all()
    return render_template('/userEnquiries.html', userEnquiries=userEnquiries[::-1], listAll=True, user=current_user, courses=courses, userEnquiryStatus=userEnquiryStatus)


#serach enquiry 
@userviews.route('/enquiries/<searchBy>/<searchConstraint>')
def userSearchEnquiry(searchBy, searchConstraint):
    print('foo')
    courses = Courses.query.with_entities(Courses.courseId, Courses.courseName).distinct().all()
    if searchBy == 'id':
        userEnquiries = Enquiries.query.filter(Enquiries.enquiryId.like("%"+searchConstraint+"%")).all()
    elif searchBy == 'name':
        userEnquiries = Enquiries.query.filter(Enquiries.enquiryCourseId.like("%"+searchConstraint+"%")).all()
    
    return render_template('/userEnquiries.html', userEnquiries=userEnquiries[::-1], courses=courses, listAll=False, user=current_user)



@userviews.route('/enrolledCourses')
def enrolledCourses():
    course_instructor = dict()
    courseIds = []
    courses = []
    category_name = dict()
    enrollments = CourseEnrollment.query.filter_by(userId=6).all()
    for enrollment in enrollments:
        courseIds.append(enrollment.courseId)
    for courseId in courseIds:
        course = Courses.query.filter_by(id=courseId).first()
        courses.append(course)
        result = Category.query.filter_by(categoryId=course.courseCategoryId).first()
        category_name[course.courseCategoryId] = result.categoryName
    for course in courses:
        instructor = Instructor.query.filter_by(instructorId=course.courseInstructorID).first()
        course_instructor[instructor.instructorId] = instructor.instructorName
    return render_template('/enrolledCourses.html', user=current_user, courses = courses, category_name=category_name,course_instructor = course_instructor)

@userviews.route('/enrolledCourses/<searchBy>/<searchConstraint>')
def userSearchEnrolledCourses(searchBy, searchConstraint):
    #user_id = current_user.userId
    user_id = 6
    page = request.args.get('page', 1, type=int)
    courses = Courses.query.with_entities(Courses.id, Courses.courseName).all()
    if searchBy == 'id':
        pass
    elif searchBy == 'name':
        return render_template('/enrolledCourses.html', user=current_user, courses=courses)
        
    return render_template('/enrolledCourses.html', user=current_user, courses=courses)
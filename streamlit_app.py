import streamlit as st

# Initialize courses and selected_courses in session state
if "courses" not in st.session_state:
    st.session_state.courses = {
        "Din Kültürü ve Ahlak Bilgisi": 4,
        "İkinci Yabancı Dil": 2,
        "Biyoloji": 4,
        "Fizik": 4,
        "Kimya": 4,
        "Matematik": 6,
        "Türk Dili ve Edebiyatı": 5,
        "Birinci Yabancı Dil": 4,
        "Beden Eğitimi": 2,
        "Resim/Müzik": 2,
        "Matematik Tarihi ve Kullanımı": 2,
        "Coğrafya": 5,
        "Çağdaş Türk ve Dünya Tarihi": 3,
    }

if "selected_courses" not in st.session_state:
    st.session_state.selected_courses = {course: False for course in st.session_state.courses}

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {course: False for course in st.session_state.courses}

# Title and instructions
st.write("# Genel Ortalama Hesaplama")
st.divider()
st.write("### Lütfen okuduğunuz dersleri soldan seçiniz")

# Sidebar for course selection
with st.sidebar:
    st.write("### Aldığım Dersler:")
    for course, coefficient in st.session_state.courses.items():
        cols = st.columns([5, 1])  # Two columns: for label and the edit button
        with cols[0]:
            # Checkbox to select courses
            st.session_state.selected_courses[course] = st.checkbox(
                f"{course} ({coefficient})", 
                value=st.session_state.selected_courses[course], 
                key=f"checkbox_{course}"
            )
        with cols[1]:
            # Smaller "Düzenle" button
            if st.button("✏️", key=f"edit_{course}"):  # Use a pencil emoji for a compact design
                st.session_state.edit_mode[course] = not st.session_state.edit_mode[course]

        # If edit mode is enabled for the course, display an input for the coefficient
        if st.session_state.edit_mode[course]:
            new_coefficient = st.number_input(
                f"{course} için yeni katsayı", 
                min_value=1, 
                max_value=10, 
                value=coefficient, 
                step=1, 
                key=f"new_coefficient_{course}"
            )
            st.session_state.courses[course] = new_coefficient  # Update the coefficient dynamically

    # Add a new course dynamically
    st.write("### Yeni Ders Ekle:")
    new_course_name = st.text_input("Ders Adı", key="new_course_name")
    new_course_coefficient = st.number_input(
        "Katsayı", 
        min_value=1, 
        max_value=10, 
        step=1, 
        value=3, 
        key="new_course_coefficient"
    )
    if st.button("Dersi Ekle", key="add_course_button"):
        if new_course_name and new_course_name not in st.session_state.courses:
            # Add the new course with its coefficient
            st.session_state.courses[new_course_name] = new_course_coefficient
            # Auto-check the new course
            st.session_state.selected_courses[new_course_name] = True
            st.session_state.edit_mode[new_course_name] = False

st.divider()

# GPA calculation logic
total_weighted_score = 0
total_coefficients = 0
for course, is_selected in st.session_state.selected_courses.items():
    if is_selected:
        # Display course header
        st.markdown(f"#### <span style='font-size: 1.5em; font-weight: bold;'>{course} Notlarınızı Girin:</span>", unsafe_allow_html=True)
        
        # Inputs for grades (default values are set to 100)
        exam1 = st.number_input(f"{course} 1. Sınav Notu:", min_value=0, max_value=100, value=100, key=f"exam1_{course}")
        exam2 = st.number_input(f"{course} 2. Sınav Notu:", min_value=0, max_value=100, value=100, key=f"exam2_{course}")
        behavior1 = st.number_input(f"{course} 1. Sözlü Notu:", min_value=0, max_value=100, value=100, key=f"behavior1_{course}")
        behavior2 = st.number_input(f"{course} 2. Sözlü Notu:", min_value=0, max_value=100, value=100, key=f"behavior2_{course}")
        
        # Toggle for adding project grade to this course
        add_project = st.checkbox(f"{course} için Proje Notu Ekle", key=f"project_toggle_{course}")
        if add_project:
            project_score = st.number_input(f"{course} Proje Notu:", min_value=0, max_value=100, value=100, key=f"project_score_{course}")
            course_average = (exam1 + exam2 + behavior1 + behavior2 + project_score) / 5
        else:
            course_average = (exam1 + exam2 + behavior1 + behavior2) / 4

        # Calculate weighted score
        weighted_score = course_average * st.session_state.courses[course]
        
        # Add to totals
        total_weighted_score += weighted_score
        total_coefficients += st.session_state.courses[course]

        # Display overall score next to the course title in bold and larger font
        st.markdown(f"**<span style='font-size: 1.2em;'>{course} Genel Puanı: {course_average:.2f}</span>**", unsafe_allow_html=True)
        
        # Add a divider for better visual separation
        st.divider()

# Final GPA calculation
if total_coefficients > 0:
    gpa = total_weighted_score / total_coefficients

    # Convert GPA to letter grade and 4.0 scale
    if gpa >= 97: letter_grade, gpa_4 = "A+", 4.0
    elif gpa >= 93: letter_grade, gpa_4 = "A", 4.0
    elif gpa >= 90: letter_grade, gpa_4 = "A-", 3.7
    elif gpa >= 87: letter_grade, gpa_4 = "B+", 3.3
    elif gpa >= 83: letter_grade, gpa_4 = "B", 3.0
    elif gpa >= 80: letter_grade, gpa_4 = "B-", 2.7
    elif gpa >= 77: letter_grade, gpa_4 = "C+", 2.3
    elif gpa >= 73: letter_grade, gpa_4 = "C", 2.0
    elif gpa >= 70: letter_grade, gpa_4 = "C-", 1.7
    elif gpa >= 67: letter_grade, gpa_4 = "D+", 1.3
    elif gpa >= 65: letter_grade, gpa_4 = "D", 1.0
    else: letter_grade, gpa_4 = "E/F", 0.0

    # Display only the numerical final GPA prominently
    st.title(f"Genel Ortalama: {gpa:.2f}")

    # Show success message with GPA letter and scale when "GPA öğren" button is clicked
    if st.button("GPA öğren"):
        st.success(f"Genel Ortalama: {gpa:.2f} ({letter_grade}), 4.0 Ölçeği: {gpa_4:.1f}")
else:
    st.warning("Lütfen ders seçin ve notları girin.")

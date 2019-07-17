import pandas as pd
import xml.etree.ElementTree as ET

lms_path = "data_original/2019-07-16-11-01-11_u0apmv5n7p.csv"

lms_data = pd.read_csv(lms_path)
list(lms_data)

# filter only Florida data
selector = 'Florida: MGT 462 '
is_fl = lms_data['Lesson'] == selector
lms_fl = lms_data[is_fl]

# Get only the columns we need
lms_fl_subset = lms_fl.filter(
    items=[
        'Last Name',
        'First Name',
        'Job Title',
        'Street Address',
        'City',
        'State/Province',
        'Postal Code',
        'Primary Phone',
        'Email',
        'Discipline ',
        'Government Level ',
        'International Status '
        ## note that there are trailing whitespace
    ]
)

# Export a CSV of filtered LMS
lms_fl_subset.to_csv(
    'data_out/lms_fl_subsetted.csv'
)

# Build the node for registration which will be appended later...
registration = ET.Element('registration')  # initialize XML node


# row_to_xml
# row: Series representing user data
# this helper function creates a new XML node
# for students, using the selected fields.
# returns: returns null.
def row_to_xml(row):
    new_student = ET.Element('student')
    new_student.set('international', row['International Status '])
    new_student.set('studentfirstname', row['First Name'])
    new_student.set('studentlastname', row['Last Name'])
    new_student.set('studentcity', row['City'])
    new_student.set('studentzipcode', row['Postal Code'])
    new_student.set('studentphone', row['Primary Phone'])
    new_student.set('discipline', row['Discipline '])
    registration.append(new_student)
    print("Appended record: " + str(row['First Name']))


# This function outputs nothing
# build_registration_xml
# df: data frame representing user data from LMS system
def build_registration_xml(df):
    df.apply(row_to_xml, axis=1)


build_registration_xml(lms_fl_subset)
tree = ET.ElementTree(registration)
tree.write('data_out/test.xml')

# Next...
# Import ZipGrade data...
eval_path = "data_original/quiz-Eval-full (1).csv"
eval_df = pd.read_csv(eval_path)
current = eval_df.head(5)
evaldata = ET.Element('evaldata')  # initialize XML node representing set of all evaluations

df_identifiers = eval_df.filter(  # Filter only the columns we want
    axis='columns',
    items=['StudentID'])
df_only_questions = eval_df.filter(  ## Filter columns by regular expressions
    axis='columns',
    regex='Stu[0-9]+')

df_cleaned = df_identifiers.join(df_only_questions)  # Join the filtered df's
df_ready = df_cleaned.assign(  # Create empty fields for written questions...
    id24='',
    id25='',
    id26='',
    id27='')

#  TODO: Create duplicate columns where question number can be identified?...

#  Rename column names to replace Stu with id
df_rename = df_ready
df_rename.columns = [col.replace('Stu', 'id') for col in df_rename.columns]

# TODO: Write helper function that takes in a row and creates an individual node
# TODO: Write function that takes in df, outputs an XML Element Tree


# make_eval_tree -> Element
# takes in a df with rows corresponding to students.
# each column is a single question. this func returns
# a tree containing a complete XML tree where
# each <evaldata> corresponds to a student and nests <question> nodes
# df: DataFrame representing evaluations
def make_eval_tree(df):
    # make_key_value -> Element
    # USED IN make_tree_from_question
    # this helper function returns an XML element <question>
    # with corresponding id=value attributes
    # ser: A Series representing a column
    # def make_key_value(key, val):
    #     xml_tag_out = ET.Element('question')
    #     q_name = ser.name  # TODO: get question name from a Series (?)
    #     q_value = ser.item  # TODO: question response value?...
    #     xml_tag_out.set(q_name, q_value)
    #     eval_out.append(xml_tag_out)  ## append it to the global eval_out
    #     return xml_tag_out
    # return {'key': 'value'}  # perhaps return a dict or array?...

    # make_tree_from_question
    # q: a Series representing a single question
    def make_tree_from_question(qs):
        # TODO: For every field in qs, make an XML tag with corresponding attribs...
        for i, v in qs.iteritems():
            xml_tag_out = ET.Element('question')
            xml_tag_out.set(str(i), str(v))  #important: must cast to strings before setting attributes...
            eval_out.append(xml_tag_out)  ## append it to the global eval_out
            #print('index: ', i, 'value: ', v)
        return eval_out  ## technically it shouldn't matter what is returned?

    eval_out = ET.Element('evaldata')
    df.apply(make_tree_from_question, axis=1)  # Apply function to all rows
    root.append(eval_out)  # don't forget to append the new evaldata to every thing
    return eval_out


root = ET.Element('evaluations')
root.append(make_eval_tree(df_rename))
out_xml = ET.ElementTree(root)
out_xml.write('data_out/test-tree2.xml')

# TODO: figure out how to fetch ID name for question
# TODO: Figure out how to fetch ID value for question

# exit()
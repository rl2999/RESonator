import pandas as pd
import xml.etree.ElementTree as et
import re
import datetime
import DataPrep


class XMLGenerator():
    in_df_lms = pd.DataFrame()
    in_df_eval = pd.DataFrame()
    in_df_meta = pd.DataFrame()
    num_students = 0  # change later
    registration = et.Element('registration')  # initialize XML node
    evaldata = et.Element('evaldata')
    el_submission = et.Element('submission')
    export_tree_final = et.ElementTree()
    out_path = 'data_out/'
    string_output_filename = ''

    string_output_file_path = ''

    def __init__(self, input_lms, input_eval, input_meta):
        """
        Instantiates a job by taking input data
        :param input_lms:
        :param input_eval:
        :param input_meta:
        """
        self.in_df_lms = input_lms
        self.in_df_eval = input_eval
        self.in_df_meta = input_meta
        self.num_students = input_lms.shape[0]
        self.string_output_filename = self.output_filename_scheme()
        self.string_output_file_path = \
            'data_out/' + self.string_output_filename + '.xml'
        print("Loaded lms data: " + str(self.in_df_lms))
        print("Loaded eval data: " + str(self.in_df_eval))
        print("Loaded meta data: " + str(self.in_df_meta))
        print('Number of students: ' + str(self.num_students))
        print('Initialized XML generator instance')

    def get_meta(self, field):
        """
        Quickly returns the metadata field from the LMS dataframe.
        :param field: String representing the field from the lms dataframe
        :return: String
        """
        df_meta = self.in_df_meta
        try:
            out_meta = str(df_meta.get(str(field)).item())
            if out_meta == 'nan':
                return ''
            else:
                return str(df_meta.get(str(field)).item())
        except:
            print("Empty field, returning empty string" + '')
            return ''

    def make_eval_tree(self, df):
        """
        takes in a df with rows corresponding to students.
        each column is a single question. this func returns
        a tree containing a complete XML tree where
        each <evaldata> corresponds to a student
        and nests <question> nodes
        :param df: DataFrame representing evaluations
        :return: none
        """
        all_evals = et.Element('evaluations')

        # make_tree_from_question -> Element
        # q: a Series representing a single question
        def make_element_from_response(qs):
            generated_eval = et.Element('evaldata')
            for i, v in qs.iteritems():  ## Loop through all questions in a row..
                # first process id's and values
                id = re.sub(r'id', '', i)
                val = str(v)
                # print('string id casting to int as: ' + str(id))
                if val != '':
                    ## If the value is empty, don't make a node for it
                    if int(id) >= 24:
                        xml_tag_out = et.Element(
                            'comment',
                            attrib={'id': id, 'answer': val})
                        generated_eval.append(
                            xml_tag_out)  # append it to the global eval_out
                    else:
                        xml_tag_out = et.Element(
                            'question',
                            attrib={'id': id, 'answer': val})
                        generated_eval.append(
                            xml_tag_out)  # append it to the global eval_out
                    # Don't create a new element if there is no need to
            all_evals.append(
                generated_eval)
            # don't forget to append the new evaldata to every thing
            return 'ok'  ## should not matter

        df.apply(make_element_from_response, axis=1)  # Apply to all rows
        export_tree_manifest = et.Element('Manifest')
        export_tree_manifest.append(self.el_submission)
        self.export_tree_final = et.ElementTree(export_tree_manifest)
        print('Finished building XML for evaluations')
        return all_evals

    def is_passed_class(inp):
        """
        calculates number of people whonumber of people who pass
        :param inp: DataFrame/Series representing a class
        :return: Boolean
        """
        if inp['Lesson Success'] == 'passed':
            return True
        else:
            return False

    def output_filename_scheme(self):
        """
        This function set up the file name scheme
        and returns a string with the appropriate values
        :return: String
        """
        # format for the xml file name is
        # TP_CourseNumber_Date_SequenceNumber.xml
        str_coursenum = self.get_meta('class_catalognum')
        date_today = datetime.datetime.today()
        str_datetime = date_today.strftime('%m%d%Y')
        output_name = \
            'NCDP' + '_' + str_coursenum + \
            '_' + str_datetime + '_' + '1'
        return output_name

    def export_final_xml(self):
        """
        wrapper function to export the xml files at the very end
        :return: none
        """
        self.export_tree_final.write(self.string_output_file_path,
                                     encoding="utf-8",
                                     xml_declaration=True)
        print('Saved RES XML as: ' + self.string_output_file_path)

    def write_doctype(self):
        """
        writes the DOCTYPE string to the first line of the output XML file

        :return:
        """
        print('Writing DOCTYPE to XML file...')
        # Read in the export file, then
        ## https://stackoverflow.com/a/10507291
        insert = '<!DOCTYPE Manifest SYSTEM "submission.dtd">'
        out_filename = self.out_path + self.output_filename_scheme() + '.xml'
        f = open(out_filename, "r")
        contents = f.readlines()
        f.close()
        contents.insert(1, insert)
        f = open(out_filename, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()
        print('Finished writing DOCTYPE string to XML file')

    def generate_xml(self):
        """
        main entry point for this class. takes 3 df inputs
        and creates an XML file from them
        :param input_lms: DataFrame
        :param input_eval: DataFrame
        :param input_meta: DataFrame
        :return: String
        """

        element_instructorpoc = et.Element(
            'instructorpoc',
            attrib={
                'instlastname':
                    self.get_meta('instructorpoc_instlastname'),
                'instfirstname':
                    self.get_meta('instructorpoc_instfirstname'),
                'instphone':
                    self.get_meta('instructorpoc_instphone')})

        el_class = et.Element(
            'class',
            attrib={
                'preparerlastname':
                    self.get_meta('class_preparerlastname'),
                'preparerfirstname':
                    self.get_meta('class_preparerlastname'),
                'batchpreparerphone':
                    self.get_meta('class_batchpreparerphone'),
                'batchprepareremail':
                    self.get_meta('class_batchprepareremail'),
                'catalognum':
                    self.get_meta('class_catalognum'),
                'classtype':
                    self.get_meta('class_classtype'),
                'classcity':
                    self.get_meta('class_classcity'),
                'classstate':
                    self.get_meta('class_state'),
                'classzipcode':
                    self.get_meta('class_classzipcode'),
                'startdate':
                    self.get_meta('class_startdate'),
                'enddate':
                    self.get_meta('class_enddate'),
                'starttime':
                    self.get_meta('class_starttime'),
                'endtime':
                    self.get_meta('class_endtime'),
                'numstudent':
                    str(self.num_students),
                'trainingmethod':
                    self.get_meta('class_trainingmethod'),
                'contacthours':
                    self.get_meta('class_contacthours')})

        eval_root = self.make_eval_tree(self.in_df_eval)
        evaluations_xml = et.ElementTree(eval_root)
        el_class.append(element_instructorpoc)
        el_class.append(self.registration)
        el_class.append(eval_root)

        el_testaverage = et.Element(
            'testaverage',
            attrib={
                'pretest':
                    self.get_meta('testaverage_pretest'),
                'posttest':
                    self.get_meta('testaverage_posttest')
            })

        el_class.append(el_testaverage)

        el_trainingprovider = et.Element(
            'trainingprovider',
            attrib={
                'tpid':
                    self.get_meta('trainingprovider_tpid'),
                'tpphone':
                    self.get_meta('trainingprovider_tpphone'),
                'tpemail':
                    self.get_meta('trainingprovider_tpemail')})
        el_trainingprovider.append(el_class)

        self.el_submission.append(el_trainingprovider)

        print('Finished generating XML with name: ' + str(
            self.string_output_filename))

        def build_registration_xml(df):
            """
            This function builds the XML node for registration info
            :param df: DataFrame to build XML from
            :return: none
            """

            def row_to_xml(row):
                """
                this helper function creates a new XML node for students
                based on the selected fields.
                :param row: Series representing user data
                :return: none
                """
                new_student = et.Element('student', attrib={
                    'international': row['International Status'],
                    'studentfirstname': row['First Name'],
                    'studentlastname': row['Last Name'],
                    'studentcity': row['City'],
                    'studentzipcode': row['Postal Code'],
                    'studentphone': row['Primary Phone'],
                    'discipline': row['Discipline'],
                    'govnlevel': row['Government Level']})
                self.registration.append(new_student)
                print("Appended record: " + str(row['First Name']))

            df.apply(row_to_xml, axis=1)
            print('Finished building XML tree for registration data')

        build_registration_xml(self.in_df_lms)
        self.export_final_xml()
        self.write_doctype()
# Higher Education Project

The goal of this project is to create and maintain a structure for large research groups in higher education. Code base solutions, contribution tracking, resource management, researcher support, and program development are included in this project. Additionally, members of this team often participate in additional projects individually, as directed. The goals of the higher education project are the following:

1) Code Management
2) Resource Management
3) Program Development

If you're a new member on this team, please read the following document: ![](https://github.com/Human-Augment-Analytics/Higher-Ed/blob/main/Higher%20Ed%20Files%20and%20Code/Higher_Ed_Final_Document.pdf)

# Code Management

When it comes to designing a system for organizing the code base of a large online research program, there are a few things to consider. First of all, the priorities of the organization must be considered. For Georgia Institute of Technology’s Human-Augmented Analytics Group, priorities include the following:

1) Code needs to be open source and easily accessible. (No “lost” code.)
2) Code contributions need to be tracked for publication attributions. 
3) Code needs to be marked as either: in-progress, tested and documented, or abandoned.
4) The instructor has to clearly be able to see the code you wrote each week.

Automated or low-human-cost solutions are preferred. In the following sections, the chosen solutions, as well as less
favorable candidates will be discussed. Future codebase managers should read section (5) for a list of the procedures required
each semester.

The following are the proposed solutions: 

1) Code needs to be open source and easily accessible. (No “lost” code.)

    Solution: Public repository in Human-Augmented-Analytics for each project, with topics added to each project for searchability.
   
    It was determined that a public repository should exist inside of Human-Augmented-Analytics for each project. This was discussed with the student researchers, and merge conflicts, repository size limits, and usability concerns for researchers were the primary reasons that this was decided. For each project repository, topics can be added, and then those topics can be searched for on the organization home page.

    ![](https://github.com/Human-Augment-Analytics/Higher-Ed/blob/main/Higher%20Ed%20Files%20and%20Code/imgs/code_base_1.PNG)

2) Code contributions need to be tracked for publication attributions. 

    Solution: Use GitHub insights. Authors who have contributed substantially to a project should be cited.

    Initially, code was written to read git logs and calculate the percentage contribution of each contributor. However, it seems much more logical to just use GitHub’s insights tab, which is attached to each repository. One can very quickly see which contributors should be cited and you can filter by commits, additions, or deletions. See the screenshot below:

    ![](https://github.com/Human-Augment-Analytics/Higher-Ed/blob/main/Higher%20Ed%20Files%20and%20Code/imgs/code_base_2.PNG)

3) Code needs to be marked as either: in-progress, tested and documented, or abandoned.
    
    Solution: Use a GitHub projects template and code tracking tag to track sections of project code.

    At first, workflow code for tagging individual files was proposed, but, when talking to student researchers, it was determined that tagging each file would probably be too tedious, especially for certain projects. Instead, each project can be broken down into sections, and we can track the progress of the code through GitHub projects. See the screenshot of the template below:

    ![](https://github.com/Human-Augment-Analytics/Higher-Ed/blob/main/Higher%20Ed%20Files%20and%20Code/imgs/code_base_3.PNG)

4) The instructor has to clearly be able to see the code you wrote each week. 

    Solution: In their report, students can give both links to the files that they worked on and screenshots of the code blocks from that week.

### Codebase Manager Responsibilities

As discussed in (1), the codebase manager needs to create or add public repositories that will house all data for each project if it does not already exist. Additionally, the codebase manager or members of each team need to add relevant topics to their repositories. These topics might include things like computer-vision, biology, or machine-learning. The codebase manager needs to make sure that projects that were set to private during development (such as competition projects) are made public at the appropriate time. Larger projects with multiple repositories must also be managed by the codebase manager as needed.

For (2), no regular actions are required by the codebase manager. When a publication needs to cite researchers for their contributions, simply go to the “Insights" tab of a repository.

As discussed in (3), the codebase manager will need to inform researchers that their code must be tracked for future reference. At the end of the semester each team's GitHub project should be checked to ensure that the team has tracked their code. Additionally, insure that all code for each team has been uploaded to the appropriate repository. Once again, the goal is to not lose any needed code. 

There is some important existing documentation for this step. First, there is both a YouTube video and pdf for explaining how teams can track their code using a “code tracking" issues tag and GitHub projects. The links are the following: YouTube (https://youtu.be/Bl0AcWL1m1k), pdf (https://github.com/Human-Augment-Analytics/Higher-Ed/blob/main/Higher%20Ed%20Files%20and%20Code/Code%20Management/GitHub%20Projects%20Documentation_%20Creating%20a%20Project%20Item.pdf). Secondly, there is documentation for creating a project from the HAAG GitHub project template: https://github.com/Human-Augment-Analytics/Higher-Ed/blob/main/Higher%20Ed%20Files%20and%20Code/Code%20Management/GitHub%20Projects%20Documentation_%20Creating%20a%20Project%20from%20HAAG%20Template.pdf. This will need to be done whenever a new repository is created.

For (4), the codebase manager simply needs to ensure that students follow the instructor's procedure for making weekly code contributions clear. This is to insure that the instructor knows that the students are contributing consistently every week.

# Resource Management

### Resource Manager Responsibilities

# Program Development

1) Mentorship Program

The mentorship program was designed to give OMSCS students interested in research at Georgia Tech opportunities to learn more about the available research programs and to get their questions answered. The mentorship program has the following objectives: 
(1) To bolster the knowledge of academic research and computer science in students who are interested.
(2) To allow students to make connections with their peers in OMSCS and to network.
(3) To allow mentors and mentees to learn from eachothers' experiences.
The mentorship program is covered at this location on the HAAG website: https://sites.gatech.edu/human-augmented-analytics-group/category/buddy-program/. The program starts with a training session for both mentors and mentees, and then mentors are asked to connect with mentees on their own. For some example materials for the mentorship program, see Kailey's mentorship slides here: https://github.com/Human-Augment-Analytics/Higher-Ed/blob/main/Higher%20Ed%20Files%20and%20Code/Program%20Development/Mentorship%20Program%20Intro%20Meeting%20Example%20Slides%20-%20Kailey%20Cozart.pdf. These slides are just an example. If someone was to use these, they would need to be updated with relevant information, such as in the "my research projects" section.

2) Seminar Program

The seminar program was designed to allow students, professors, and others to share specific information about their area of expertise. This program allows both presenters and listeners to grow and learn. The seminar program has the following objectives: 
(1) To help students learn more about their peers in the Human Augmented Analytics Group.
(2) To encourage learning from others about scholarly topics.
(3) To facilitate discussions about scholarly topics.
During its first semester, the seminar program hosted 5 seminars. For reference, previous seminars are available for viewing on the HAAG website: https://sites.gatech.edu/human-augmented-analytics-group/category/seminars/.

### Program Development Manager Responsibilities

The program manager oversees the buddy program and the seminar program. For the mentorship program, the program development manager will be responsible for recruiting mentees, leading the training session, potentially providing materials for mentors to use, and following up with mentors to assure that they have adequately engaged with their mentees. For the seminar program, the program development manager will be responsible for recruiting presenters for the program, hosting the seminars, and archiving them on the website for future viewing.

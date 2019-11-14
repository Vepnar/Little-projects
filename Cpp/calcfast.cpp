// Author: Arjan de Haan (Vepnar)
// This is some script that will test that will measure how fast you can solve basic math problems 

#include <iostream>
#include <string>
#include <chrono>
#include <sstream>


// Here we will ask the user to answer the question with a number.
int ask_question(std::string question)
{
    // First we will show the question to the user.
    // So they know what question they're answering.
    std::cout << question << std::endl;
    std::cout << "> ";

    // Then we make a string where we can store the user their answer in.
    std::string in;

    // After we created the string we can capture the user their input as string.
    // We capture the user their input from the terminal/console.
    std::getline(std::cin, in);
        
    // After we captured our answer we need to convert it to a number.
    // That's what happening here.
    return std::atoi(in.c_str());
     
}

// Here we will generate the easy questions.
// The questions will only contain easy addition, subtraction and multiplication.
std::pair<std::string, int> generate_easy_question()
{
    // Generate a random number between 1-3 to select a random kind of question
    int option = rand() % 3 + 1;

    // We also need a place to store te generated answer and the generated question
    int answer;
    std::string question;

    // We also already generate both terms random and between 1-10 for the questions
    // So we don't have to do that every single time for each question generated
    int term1 = rand() % 10 + 1;
    int term2 = rand() % 10 + 1;
    
    switch(option)
    {
        // Case 1 is the case were we will generate the addition question
        case 1:

        // We first calculate the answer
        answer = term1+ term2;
        
        // Then we will set the question value to a plus sign
        // We will format this later into a beautiful string
        question = "+";
        break;

        // Case 2 is the subtraction question.
        case 2:

        // We first need to look which term is more.
        // Because we don't want any negative numbers.
        if (term2 > term1)
        {
            // When term 2 is more than term 1 we actually got some kind of problem
            // Because we don't want negative values.
            // So we have to switch term1 and term 2 around.

            // This is a silly trick to switch the values around
            // Without using a third variable
            term1 = term1+term2;
            term2 = term1-term2;
            term1 = term1-term2;

            // Now we can go on and make the question like normal
        }
        // Like before we calculate the answer
        answer = term1 - term2;

        // Then we set the minus sign again for the later formatting
        question = "-";
        break;

        // Case 3. The case about multiplication.
        // Multiplications are easier than subtractions because we dont have to deal with negative numbers.
        // First of all terms are not called terms for Multiplications they are called factors
        // It doesn't really matter for variable names but it is just something you should keep in the back of your head
        case 3:

        // This is almost the same as additions but with a '*' sign.
        answer = term1 * term2;

        // We used a cross symbole for multiplications because it looks better than an asterisk.
        question = "×";
        break;
    }

    // Now we will format the string in some pretty way
    // We first begin with creating a stream for the strings to be stored in
    std::stringstream ss;
    
    // Now we add our terms and question sign
    ss << term1 << " " << question << " " << term2 << " = ?";

    // After that we convert our string stream back into a string and store it in the question string
    question = ss.str();

    // Now we make a pair to store the question and the answer in
    // And return it so it could be used in the next function
    return std::make_pair(question, answer);


}


int main(void)
{
    // We first start with setting up our random number generator.
    // We will need this later to generate random questions for the user.
    srand (time(NULL));

    // Now we start the test with 10 questions
    // But first we will start a timer to see how much time it takes for you to answer the questions
    auto start_time = std::chrono::high_resolution_clock::now();

    for(int i=0;i<10;i++)
    {

        // Now we will generate a question
        std::pair<std::string, int> question_set = generate_easy_question();

        // Now we got the question now we have to ask the question in an infinite loop
        // The user can only leave this infinite loop when the answer the question correct
        while (true) {

            // First we clear the terminal because it's looks better
            // This might not work on windows but it does work on unix based systems
            std::cout << "\033c";

            // Now we ask the question to the user and store their answer in a variable
            int answer = ask_question(question_set.first);

            // After we done al that we need to check if the answer is correct
            // Cancel the loop when the answer is correct
            if( answer == question_set.second ) break;
        }

        // Now we go to the next question
    }
    
    // Measure the current time and calculate how much time the user took to complete the test in seconds
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>( end_time - start_time ).count();

    // Print the spend time to the user.
    // This time is in seconds and not completely accurate because we also measured the time the system took to generate the questions.
    std::cout << "You took: " << duration << " seconds to complete the test\n";
    
}



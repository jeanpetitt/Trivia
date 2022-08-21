import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      nb_page: 0,
      page: 2,
      totalQuestions: 0,
      categories: {},
      okay:{},
      currentCategory: null,
      t:""
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.totalQuestions,
          categories: result.categories,
          currentCategory: result.current_category,
          nb_page: result.nbre_page })
        return;  
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  } 

  createPagination(){
    let pageNumbers = [];
    let maxPage = this.state.nb_page
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.totalQuestions,
           
          
        })
        console.log(this.setState.questions, "true good job")
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        console.log(this.state.questions,"fail")
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions/search`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({search: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}/delete`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }
  
  render() {
    // creons un objet constant qui vas stocke la liste de dictionnaire
    // key={id, type}
    const obj = this.state.categories
    var arr;
    if (obj){
      //  creer un tableau de liste contenant les key={id, type} permettant
      // de rendre plus facile le map
      arr = Object.values(obj)
      console.log('list arry', arr)
    }
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {arr.map(cat => (
              <li key={cat.id} onClick={() => {this.getByCategory(cat.id)}}>
                {cat.id}
                <img className="category" src={`${cat.type}.svg`} alt={`${cat.type} category`}/>
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
         <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => 
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={q.category}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          )}

          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;


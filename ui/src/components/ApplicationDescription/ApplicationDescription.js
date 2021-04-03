import React from "react";
import sentimentformula from "./sentimentformula.png";
import image7 from "../../images/07.png";
import { Grid } from "@material-ui/core";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Typography from "@material-ui/core/Typography";
import books from "../../images/noun_books_137857.png";
import emotion from "../../images/noun_emotions_582951.png";
import result from "../../images/noun_result_3265903.png";
import thinking from "../../images/noun_Thinking_2082981.png";
import posneg from "../../images/noun_perspective_1544047.png";
import agree from "../../images/noun_Agree_3813416.png";

const ApplicationDescription = () => {
  return (
    <div className="description-container" data-testid="description-container">
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: "100vh" }}
      >
        <Grid
          container
          spacing={0}
          direction="row"
          alignItems="center"
          justify="center"
          className="welcome-background"
        >
          <Grid item xs={6} container alignItems="center" justify="center">
            <div className="welcome-desc">
              <h4 className="homepage-titles">About</h4>
              <p className="homepage-desc">
                James is a tool for research in the Digital Humanities that
                combines LDA topic modelling and sentiment analysis to analyze
                attitudes towards topics present in text. You can process a
                single document to analyze the topics present within, and the
                attitudes towards those topics. You can also process multiple
                documents together in order to understand the way the attitudes
                towards the same topics differ between texts.
              </p>
            </div>
          </Grid>
          <Grid item xs={3} container>
            <img src={image7} className="welcome-image" alt="about-james"></img>
          </Grid>
        </Grid>

        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          className="howto-background"
        >
          <div className="howto-desc">
            <h4 className="homepage-titles">How to Use James</h4>
            <Grid
              container
              spacing={3}
              direction="row"
              alignItems="stretch"
              justify="center"
            >
              <Grid item xs={3}>
                <Card className="howto-card">
                  <CardMedia
                    className="howto-card-media"
                    component="img"
                    style={{ height: 200 }}
                    image={books}
                    title="Click to upload"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="h2">
                      1. Upload your texts
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      Click on the upload button to select the text(s) you would
                      like to analyze. You can select one or more documents, but
                      they must all be text (.txt) files. Please note that you
                      can't upload your files one at a time; they must all be
                      uploaded at once.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={3}>
                <Card className="howto-card">
                  <CardMedia
                    className="howto-card-media"
                    component="img"
                    style={{ height: 200 }}
                    image={thinking}
                    title="Click to upload"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="h2">
                      2. Enter topic number
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      Enter the number of topics you would like the model to
                      generate for your uploaded text(s). This must be a number
                      between 1 and 200.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={3}>
                <Card className="howto-card">
                  <CardMedia
                    className="howto-card-media"
                    component="img"
                    style={{ height: 200 }}
                    image={emotion}
                    title="Click to upload"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="h2">
                      3. Choose Sentiment Analysis
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      Use the dropdown list to select the dataset you would like
                      to use for the sentiment analysis model.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={3}>
                <Card className="howto-card">
                  <CardMedia
                    className="howto-card-media"
                    component="img"
                    style={{ height: 200 }}
                    image={result}
                    title="Click to upload"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="h2">
                      4. Get your results!
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      Click Calculate! It may take several minutes for James to
                      process your results, especially if you uploaded a large
                      volume of text.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
            <p className="howto-note">
              <b>Please note:</b> James was designed and trained using English
              text; while James will allow you to upload documents containing
              text in other languages, the results will certainly be unintended.
              <br />
              Also, please ensure that your uploaded text is long enough for the
              number of selected topics; if the input is too short, it is
              impossible to generate a topic model. If your results contain any
              topics that have no associated words, your number of topics is too
              high!
            </p>
          </div>
        </Grid>
        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          className="understand-background"
        >
          <div className="understand-desc">
            <h4 className="homepage-titles">Understanding the Results</h4>
            <Grid
              container
              spacing={0}
              direction="row"
              alignItems="center"
              justify="center"
            ></Grid>
            <p>
              Once James has finished processing your input, you will see the
              results displayed on the screen. You also have the option to
              download your results as a .csv file using the 'Download Results'
              button at the very top of the page.
              <br />
              <br />
              At the top of the results, you'll see the list of topics generated
              by the topic model for your input text. Each of these topics will
              be numbered for identification. Immediately below the topic
              number, you'll find a button that allows you to hide or show each
              topic from the results. For each topic, the results contain two
              things that will help you understand the topic's meaning: words
              and example sentences. <br />
              First, you'll see a collection of the top words that the topic
              model has identified as belonging to this topic. The topic model
              actually uses word stems to generate each topic, but to make the 
              results easier to understand, we provide both an example of a word 
              from the text that produced each stem along with the stem itself. 
              Each word is also given a weight, which represents how important 
              that word is for the given topic.
              <br />
              Finally, each topic will have up to 5 example sentences from your
              input text that had the highest weight towards that topic, along
              with that weight.
              <br />
              <br />
              After the topic model results comes the document analysis. Here,
              you'll see a list of documents, and for each document a list of
              topics. For each topic, the list will show the topic number, that
              topic's weight in the given document, and the document's sentiment
              towards that topic. Both of these values will be numbers between 0 
              and 1. The topic weight represents the presence of that topic in the 
              given document, so the topic weight of all topics will sum to 1. The 
              meaning of the sentiment value depends on your chosen sentiment model: 
              if you chose Support-Oppose, 1 represents support and 0 represents 
              oppose. Likewise, if you chose Positive-Negative, 1 represents 
              positive, and 0 represents negative.
              <br /> <br />
              Please note: Once you leave this page, your results will be lost.
              Be sure to download your results if you want to refer to them
              later!
            </p>
          </div>
        </Grid>
        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          className="how-background"
        >
          <div className="how-desc">
            <h4 className="homepage-titles">How It Works</h4>
            <p>
              James uses the <a href="http://mallet.cs.umass.edu/">MALLET</a>{" "}
              implementation of{" "}
              <a href="https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation">
                Latent Dirichlet Allocation
              </a>{" "}
              for topic modelling.
              <br />
              <br />
              Coherence scores for each topic are a measure of the relative
              distance between words within a topic; that is, the likelihood
              that words belonging to that topic will be found together. We are
              using C_V coherence scores, which are a number between 0 and 1.
              <br />
              The overall coherence score for the topic model is an average of
              the coherence scores for each topic. Since the number of topics is
              specified by the user, this score can be a helpful metric to judge
              whether the chosen number of topics is appropriate for the input
              text.
              <br />
              For more information, check out{" "}
              <a href="https://datascienceplus.com/evaluation-of-topic-modeling-topic-coherence/">
                this article
              </a>
              .
            </p>
            <p className="how-text">
              The sentiment analysis utilizes{" "}
              <a href="https://www.tensorflow.org/api_docs/python/tf/keras/layers/RNN">
                tensorflow's{" "}
              </a>
              implementation of a recurrent neural network with{" "}
              <a href="https://en.wikipedia.org/wiki/Long_short-term_memory">
                LTSM{" "}
              </a>
              architecture. There are 2 models:
            </p>
            <Grid
              container
              spacing={3}
              direction="row"
              alignItems="center"
              justify="center"
              className="how-softwareimages"
            >
              <Grid item xs={4}>
                <Card className="how-card">
                  <CardMedia
                    className="how-card-media"
                    component="img"
                    style={{ height: "60%" }}
                    image={posneg}
                    title="Model 1"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="h2">
                      Positive - Negative
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      This model was trained on thousands of{" "}
                      <a href="https://www.kaggle.com/marklvl/sentiment-labelled-sentences-data-set">
                        amazon, yelp and imdb reviews
                      </a>{" "}
                      and is capable of predicting the binary sentiment
                      (positive or negative) of a piece of text.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={4}>
                <Card className="how-card">
                  <CardMedia
                    className="how-card-media"
                    component="img"
                    src={agree}
                    style={{ height: "60%" }}
                    title="Model 1"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6" component="h2">
                      Support - Oppose
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      This model was trained on{" "}
                      <a href="https://www.cs.cornell.edu/home/llee/data/convote.html">
                        US congressional floor debates{" "}
                      </a>{" "}
                      and is able to predict whether a piece of text is
                      demonstrating support or opposition.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <p className="how-text">
              For each topic in each document, the sentiment towards that topic
              is calculated using the following formula:
            </p>
            <img
              className="sentiment-formula"
              src={sentimentformula}
              alt="sentiment formula"
            />
            <p>
              Where t(sentence) is the topic weight of the sentence towards the
              given topic, given by the topic model, and s(sentence) is the
              sentiment of the sentence, given by the sentiment analysis model.
              <br />
              <br />
              James is an Open Source project hosted on{" "}
              <a href="https://github.com/myrithok/James">github</a>. Detailed
              information about the project's design and requirements can be
              found on the{" "}
              <a href="https://github.com/myrithok/James/wiki">wiki</a> there.
            </p>
          </div>
        </Grid>
        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          className="authors-background"
        >
          <div className="authors-desc">
            <h4 className="homepage-titles">Who We Are</h4>
            <p>
              James was developed by Andrew Mitchell, Esam Haris, Indika
              Wijesundera, Robert Vardy, and Samuel Alderson for Dr. Alexander
              Klein as their Computer Science Capstone Project at McMaster
              University.
            </p>
          </div>
        </Grid>
        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          className="extras-background"
        >
          <div className="extra-desc">
            <h4>Help Us Improve</h4>
            <p>
              If you would like to report a software bug, make a suggestion on
              how we can improve the app, or have any other requests, feel free
              to create an issue on the James{" "}
              <a href="https://github.com/myrithok/James/issues">github</a>.
            </p>
            <h4>Acknowledgements</h4>
            <p>
              McCallum, Andrew Kachites. "MALLET: A Machine Learning for
              Language Toolkit. "http://mallet.cs.umass.edu. 2002.
              <br />
              <br />
              Lee, Lillian. "Congressional speech
              data".https://www.cs.cornell.edu/home/llee/data/convote.html.
              2008.
              <br />
              <br />
              Kotzias, Dimitrios. "From Group to Individual Labels using Deep
              Features".https://www.kaggle.com/marklvl/sentiment-labelled-sentences-data-set.
              2015
              <br />
              <br />
            </p>
          </div>
        </Grid>
      </Grid>
    </div>
  );
};

export default ApplicationDescription;

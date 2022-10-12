# syntax=docker/dockerfile:1
FROM ruby:2.4.2
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.li
RUN apt-get update -qq && apt-get install -y nodejs yarn
WORKDIR /Users/ezgovind/Documents/ruby/test-interview-question-master
COPY Gemfile /Users/ezgovind/Documents/ruby/test-interview-question-master/Gemfile
COPY Gemfile.lock /Users/ezgovind/Documents/ruby/test-interview-question-master/Gemfile.lock
RUN bundle install

# Add a script to be executed every time the container starts.
COPY package.json /calculator/package.json
COPY yarn.lock /Users/ezgovind/Documents/ruby/test-interview-question-master/yarn.lock
RUN yarn install --check-files
COPY . /test-interview-question-master/
# COPY /Users/ezgovind/Documents/ruby/test-interview-question-master/entrypoint.sh /usr/bin/
# RUN chmod +x /usr/bin/entrypoint.sh
# ENTRYPOINT ["entrypoint.sh"]
EXPOSE 3000

# Configure the main process to run when running the image
CMD ["rails", "server", "-b", "0.0.0.0"]
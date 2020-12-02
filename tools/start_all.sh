#!/bin/bash

cd postgres && make setupdb && cd - && cd rabbitmq && make up && cd - && cd .. && make migrate && echo 'FINISHED!'

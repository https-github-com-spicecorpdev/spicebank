#!/bin/bash

rm backend/templates/*

cp frontend/*.html backend/templates

rm backend/static/styles/*

cp frontend/css/*.css backend/static/styles

rm backend/static/img/*

cp frontend/imagens/* backend/static/img

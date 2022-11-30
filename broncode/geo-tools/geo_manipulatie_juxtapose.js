/* juxtapose - v1.2.2 - 2020-09-03
 * Copyright (c) 2020 Alex Duner and Northwestern University Knight Lab
 */
/* juxtapose - v1.1.2 - 2015-07-16
 * Copyright (c) 2015 Alex Duner and Northwestern University Knight Lab
 */
/*
 * Veel code weggehaald om de slider met kaarten te laten samenwerken
 */

(function (document, window) {

    var juxtapose = {
        sliders: [],
        OPTIMIZATION_ACCEPTED: 1,
        OPTIMIZATION_WAS_CONSTRAINED: 2
    };

    function addClass(element, c) {
        if (element.classList) {
            element.classList.add(c);
        } else {
            element.className += " " + c;
        }
    }

    function removeClass(element, c) {
        element.className = element.className.replace(/(\S+)\s*/g, function (w, match) {
            if (match === c) {
                return '';
            }
            return w;
        }).replace(/^\s+/, '');
    }

    function setText(element, text) {
        if (document.body.textContent) {
            element.textContent = text;
        } else {
            element.innerText = text;
        }
    }

    function getComputedWidthAndHeight(element) {
        if (window.getComputedStyle) {
            return {
                width: parseInt(getComputedStyle(element).width, 10),
                height: parseInt(getComputedStyle(element).height, 10)
            };
        } else {
            w = element.getBoundingClientRect().right - element.getBoundingClientRect().left;
            h = element.getBoundingClientRect().bottom - element.getBoundingClientRect().top;
            return {
                width: parseInt(w, 10) || 0,
                height: parseInt(h, 10) || 0
            };
        }
    }

    function viewport() {
        var e = window,
            a = 'inner';
        if (!('innerWidth' in window)) {
            a = 'client';
            e = document.documentElement || document.body;
        }
        return { width: e[a + 'Width'], height: e[a + 'Height'] }
    }

    function getPageX(e) {
        var pageX;
        if (e.pageX) {
            pageX = e.pageX;
        } else if (e.touches) {
            pageX = e.touches[0].pageX;
        } else {
            pageX = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        }
        return pageX;
    }

    function getPageY(e) {
        var pageY;
        if (e.pageY) {
            pageY = e.pageY;
        } else if (e.touches) {
            pageY = e.touches[0].pageY;
        } else {
            pageY = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        return pageY;
    }

    function getLeftPercent(slider, input) {
        if (typeof (input) === "string" || typeof (input) === "number") {
            leftPercent = parseInt(input, 10);
        } else {
            var sliderRect = slider.getBoundingClientRect();
            var offset = {
                top: sliderRect.top + document.body.scrollTop + document.documentElement.scrollTop,
                left: sliderRect.left + document.body.scrollLeft + document.documentElement.scrollLeft
            };
            var width = slider.offsetWidth;
            var pageX = getPageX(input);
            var relativeX = pageX - offset.left;
            leftPercent = (relativeX / width) * 100;
        }
        return leftPercent;
    }

    function JXSlider(selector, width, height, onSlide) {

        this.selector = selector;
        this._OnSlide = onSlide;
        this.width = width;
        this.height = height;
        this.aspect = (this.width / this.height);
        this._onLoaded();
    }

    JXSlider.prototype = {

        updateSlider: function (input, animate) {
            var leftPercent, rightPercent;

            leftPercent = getLeftPercent(this.slider, input);

            var sliderPos = (leftPercent * this.width) / 100;
            leftPercent = leftPercent.toFixed(2) + "%";
            leftPercentNum = parseFloat(leftPercent);
            rightPercent = (100 - leftPercentNum) + "%";

            if (leftPercentNum > 0 && leftPercentNum < 100) {
                removeClass(this.handle, 'transition');

                this._OnSlide(sliderPos);
                this.handle.style.left = leftPercent;
                this.sliderPosition = leftPercent;
            }
        },

        getPosition: function () {
            return this.sliderPosition;
        },

        displayLabel: function (element, labelText) {
            label = document.createElement("div");
            label.className = 'jx-label';
            label.setAttribute('tabindex', 0); //put the controller in the natural tab order of the document

            setText(label, labelText);
            element.appendChild(label);
        },

        calculateDims: function (width, height) {
            var ratio = this.aspect;
            if (width) {
                height = width / ratio;
            } else if (height) {
                width = height * ratio;
            }
            return {
                width: width,
                height: height,
                ratio: ratio
            };
        },

        setWrapperDimensions: function () {
            var wrapperWidth = getComputedWidthAndHeight(this.wrapper).width;
            var wrapperHeight = getComputedWidthAndHeight(this.wrapper).height;
            var dims = this.calculateDims(wrapperWidth, wrapperHeight);

            this.wrapper.style.height = parseInt(dims.height) + "px";
            this.wrapper.style.width = parseInt(dims.width) + "px";
        },

        optimizeWrapper: function (maxWidth) {
            var result = juxtapose.OPTIMIZATION_ACCEPTED;
            if (this.width >= maxWidth) {
                this.wrapper.style.width = maxWidth + "px";
                result = juxtapose.OPTIMIZATION_WAS_CONSTRAINED;
            } else {
                this.wrapper.style.width = this.width + "px";
            }
            this.setWrapperDimensions();
            return result;
        },

        _onLoaded: function () {

            this.wrapper = document.querySelector(this.selector);
            addClass(this.wrapper, 'juxtapose');

            this.wrapper.style.width = this.width;
            this.setWrapperDimensions();

            this.slider = document.createElement("div");
            this.slider.className = 'jx-slider';
            this.wrapper.appendChild(this.slider);

            this.handle = document.createElement("div");
            this.handle.className = 'jx-handle';

            this.slider.appendChild(this.handle);

            this.leftArrow = document.createElement("div");
            this.rightArrow = document.createElement("div");
            this.control = document.createElement("div");
            this.controller = document.createElement("div");

            this.leftArrow.className = 'jx-arrow jx-left';
            this.rightArrow.className = 'jx-arrow jx-right';
            this.control.className = 'jx-control';
            this.controller.className = 'jx-controller';

            this.controller.setAttribute('tabindex', 0); //put the controller in the natural tab order of the document
            this.controller.setAttribute('role', 'slider');
            this.controller.setAttribute('aria-valuenow', 50);
            this.controller.setAttribute('aria-valuemin', 0);
            this.controller.setAttribute('aria-valuemax', 100);

            this.handle.appendChild(this.leftArrow);
            this.handle.appendChild(this.control);
            this.handle.appendChild(this.rightArrow);
            this.control.appendChild(this.controller);

            this._init();
        },

        _init: function () {

            this.updateSlider("50%", false);

            var self = this;
            window.addEventListener("resize", function () {
                self.setWrapperDimensions();
            });


            // Set up Javascript Events
            // On mousedown, call updateSlider then set animate to false
            // (if animate is true, adds css transition when updating).

            this.slider.addEventListener("mousedown", function (e) {
                e = e || window.event;
                e.preventDefault();
                self.updateSlider(e, true);
                animate = true;

                this.addEventListener("mousemove", function (e) {
                    e = e || window.event;
                    e.preventDefault();
                    if (animate) { self.updateSlider(e, false); }
                });

                this.addEventListener('mouseup', function (e) {
                    e = e || window.event;
                    e.preventDefault();
                    e.stopPropagation();
                    this.removeEventListener('mouseup', arguments.callee);
                    animate = false;
                });
            });

            this.slider.addEventListener("touchstart", function (e) {
                e = e || window.event;
                e.preventDefault();
                e.stopPropagation();
                self.updateSlider(e, true);

                this.addEventListener("touchmove", function (e) {
                    e = e || window.event;
                    e.preventDefault();
                    e.stopPropagation();
                    self.updateSlider(event, false);
                });

            });

            /* keyboard accessibility */

            this.handle.addEventListener("keydown", function (e) {
                e = e || window.event;
                var key = e.which || e.keyCode;
                var ariaValue = parseFloat(this.style.left);

                //move jx-controller left
                if (key == 37) {
                    ariaValue = ariaValue - 1;
                    var leftStart = parseFloat(this.style.left) - 1;
                    self.updateSlider(leftStart, false);
                    self.controller.setAttribute('aria-valuenow', ariaValue);
                }

                //move jx-controller right
                if (key == 39) {
                    ariaValue = ariaValue + 1;
                    var rightStart = parseFloat(this.style.left) + 1;
                    self.updateSlider(rightStart, false);
                    self.controller.setAttribute('aria-valuenow', ariaValue);
                }
            });

            juxtapose.sliders.push(this);
        }

    };

    /*
      Given an element that is configured with the proper data elements, make a slider out of it.
    */
    juxtapose.makeSlider = function (elt, width, height, onSlide) {
        var idx = juxtapose.sliders.length; // not super threadsafe...
        specificClass = 'juxtapose-' + idx;
        addClass(elt, specificClass);
        slider = new juxtapose.JXSlider('.' + specificClass, width, height, onSlide);
    };

    juxtapose.JXSlider = JXSlider;
    window.juxtapose = juxtapose;
}(document, window));


// addEventListener polyfill / jonathantneal
!window.addEventListener && (function (WindowPrototype, DocumentPrototype, ElementPrototype, addEventListener, removeEventListener, dispatchEvent, registry) {
    WindowPrototype[addEventListener] = DocumentPrototype[addEventListener] = ElementPrototype[addEventListener] = function (type, listener) {
        var target = this;

        registry.unshift([target, type, listener, function (event) {
            event.currentTarget = target;
            event.preventDefault = function () { event.returnValue = false };
            event.stopPropagation = function () { event.cancelBubble = true };
            event.target = event.srcElement || target;

            listener.call(target, event);
        }]);

        this.attachEvent("on" + type, registry[0][3]);
    };

    WindowPrototype[removeEventListener] = DocumentPrototype[removeEventListener] = ElementPrototype[removeEventListener] = function (type, listener) {
        for (var index = 0, register; register = registry[index]; ++index) {
            if (register[0] == this && register[1] == type && register[2] == listener) {
                return this.detachEvent("on" + type, registry.splice(index, 1)[0][3]);
            }
        }
    };

    WindowPrototype[dispatchEvent] = DocumentPrototype[dispatchEvent] = ElementPrototype[dispatchEvent] = function (eventObject) {
        return this.fireEvent("on" + eventObject.type, eventObject);
    };
})(Window.prototype, HTMLDocument.prototype, Element.prototype, "addEventListener", "removeEventListener", "dispatchEvent", []);

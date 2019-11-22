function ImportButton(root, opts) {
  var defaults = {
    compiler_import_url: "",
    clone_url: "",
    is_library: false,
    last_used_action: {
      type: "compiler",
    },
    cli_enabled: false,
  }
  opts = $.extend({}, defaults, opts);

  // Default state
  this.state = {
    collapsed: true,
    workspaces: [],
    action: {},
    userChangedIDE: false,
  }

  this.setState = function(o, trigerUpdate) {
    if (trigerUpdate == null) {
      trigerUpdate = true;
    }
    var prevState = this.state;
    this.state = $.extend({}, this.state, o);
    if (trigerUpdate) {
      this.onNewState(prevState, this.state);
    }
  }.bind(this);

  this.initialize = function() {
    // Register clipboard listeners
    new Clipboard('.clippy-btn');
    // Set action from params as state
    this.setState({
      action: opts.last_used_action
    });
  }.bind(this);

  this.conditionalRenderDropdown = function(state) {
    // Initial render
    this.renderDropdown();
  }

  this.getCookie = function(name) {
    if(document.cookie.length > 0) {
      var c_start = document.cookie.indexOf(name + "=");
      if(c_start != -1) {
        c_start = c_start + name.length + 1;
        var c_end = document.cookie.indexOf(";", c_start);
        if(c_end == -1) c_end = document.cookie.length;
        return unescape(document.cookie.substring(c_start,c_end));
      }
    }
    return "";
  }

  this.onNewState = function(prevState, newState) {
    if (prevState.collapsed != newState.collapsed) {
      $("#dropdown-content").toggle();
      this.conditionalRenderDropdown(newState);
    }

    // If the action component changes it means we've changed IDE preference
    if (JSON.stringify(prevState.action) !== JSON.stringify(newState.action) || newState.userChangedIDE) {
      this.setState({ collapsed: true }, false);
      this.render();
      // Check if we're on the initial render, in which case this state change isn't that important
      if (newState.userChangedIDE) {
        this.setState({
          userChangedIDE: false
        }, false);

        $.ajax({
          url: '/api/v3/userinfo/',
          data: JSON.stringify({
            "profile": {
              "default_editor": newState.action.type,
            }
          }),
          type: "PATCH",
          contentType: "application/json; charset=utf-8",
          dataType: 'json',
          headers: {
            "X-CSRFToken": this.getCookie("csrftoken")
          }
        })

        // Now we just emulate the click on the button
        $('#import-button-action')[0].click();
      }
    }

  }.bind(this);

  this.handleToggleClick = function(e) {
    this.setState({
      collapsed: !this.state.collapsed,

    })
  }.bind(this);

  this.getActionLabel = function(ide) {
    var label;
    switch(ide) {
      case "compiler":
        label = "Import into Compiler";
        break;
      case "cli":
        label = "Import with CLI";
        break;
      case "studio":
        label = "Import with Mbed Studio";
        break;
      default:
        break;
    }
    return label;
  };

  this.getActionTarget = function(ide) {
    var target;
    switch(ide) {
      case "compiler":
        target = opts.compiler_import_url;
        break;
      case "cli":
      case "studio":
        target = "#";
        break;
      default:
        break;
    }
    return target;
  };

  this.handleIDEChange = function(e, action) {
    this.setState({
      action: action,
      userChangedIDE: true
    })
  }.bind(this);

  this.newIDEElement = function(text, action, immediateAction, classes, callback, newWindow) {
    // Default to open in new window/tab
    newWindow = typeof newWindow === 'undefined' ? true : newWindow;

    var li = $("<li></li>").addClass("ide-element")

    // Bind default click callback changing the user IDE preference
    if (immediateAction === null || ! $.isEmptyObject(action)) {
      li.bind("click", function(e) { e.preventDefault(); this.handleIDEChange(e, action) }.bind(this));
    }

    li.append( 
      $("<a></a>")
      .attr({
        href: immediateAction ? immediateAction : "#",
        target: newWindow ? "_blank" : "_self"
      })
      .addClass(["ide-link", classes].join(" "))
      .text(text)
    );

    // Custom callback, if we want to do something special on click
    if (callback) {
      li.bind('click', callback);
    }

    return li;
  }

  this.getClassicBlock = function() {
    return this.newIDEElement("Import into Compiler", {
      type: "compiler"
    }, null, "lock")
  }

  this.renderCLIDropdown = function() {
    $('#dropdown-content').toggle();
    var cliInput = opts.is_library ? 'mbed add' : 'mbed import';
    cliInput = cliInput + " " + opts.clone_url;
    $('#dropdown-content').html(
        $('<div></div>)')
          .addClass('mbed-cli-wrapper')
          .html(
            [
              $('<h5></h5>').text('Importing project with mbed CLI'),
              $('<p></p>').text('This is how you do it:'),
              $('<input></input>')
                .attr({ id: 'mbed-cli-input', value: cliInput }),
              $('<button></button>')
                .addClass('clippy-btn')
                .attr({
                  'data-clipboard-target': '#mbed-cli-input'
                }),
              $('<a></a>')
                .attr({
                  href: 'https://docs.mbed.com/docs/mbed-os-handbook/en/5.1/dev_tools/cli/',
                  target: '_blank'
                })
                .text('Instructions for installing mbed CLI')
            ]
          )
    );
  },

  this.cliCallback = function(e) {
    e.preventDefault();
    this.renderCLIDropdown();
    return false;
  }.bind(this);

  this.getCliBlock = function() {
    return this.newIDEElement("Import with mbed CLI", {
      type: "cli"
    })
  };

  this.renderStudioDropdown = function() {
    $('#dropdown-content').toggle();
    var heading;
    var instructions;
    if (opts.is_library) {
      heading = 'Importing library with Mbed Studio';
      instructions = 'Use the following link in "File -> Add Library to Active Program..."';
    } else {
      heading = 'Importing program with Mbed Studio';
      instructions = 'Use the following link in "File -> Import Program"';
    }
    $('#dropdown-content').html(
        $('<div></div>)')
          .addClass('mbed-cli-wrapper')
          .html(
            [
              $('<h5></h5>').text(heading),
              $('<p></p>').text(instructions),
              $('<input></input>')
                .attr({ id: 'mbed-studio-input', value: opts.clone_url  }),
              $('<button></button>')
                .addClass('clippy-btn')
                .attr({
                  'data-clipboard-target': '#mbed-studio-input'
                }),
              $('<a></a>')
                .attr({
                  href: 'https://os.mbed.com/studio/',
                  target: '_blank'
                })
                .text('Download Mbed Studio')
            ]
          )
    );
  };

  this.studioCallback = function(e) {
    e.preventDefault();
    this.renderStudioDropdown();
  }.bind(this);


  this.getStudioBlock = function() {
    return this.newIDEElement("Import into Mbed Studio", {
      type: "studio"
    })
  };

  this.renderDropdown = function() {
    var ul = $("<ul></ul>").addClass('import-dropdown');

    var blocks = $();
    blocks = blocks.add(this.getClassicBlock());
    if (opts.cli_enabled) {
      blocks = blocks.add(this.getCliBlock());
    }
    blocks = blocks.add(this.getStudioBlock());


    ul.append(blocks)
    $("#dropdown-content").html(ul);
  }

  this.getActionButton = function() {
    var label = this.getActionLabel(this.state.action.type);
    var target = this.getActionTarget(this.state.action.type);
    var callbacks = {
      'cli': this.cliCallback,
      'studio': this.studioCallback,
    };
    var callback = callbacks[this.state.action.type];

    var b = $('<a></a>')
      .addClass('import-button-a')
      .attr({
        'id': 'import-button-action',
        'href': target,
        'target': '_blank'
      })
      .text(label);
    if (callback) {
      b.bind('click', callback);
    }
    return b;

  }.bind(this)

  this.newDropdown = function() {
    return $('<div></div>')
      .attr({
        'id': 'dropdown-content',
      })
  }

  this.render = function() {
    // Dropdown content (initially hidden, and empty)
    var dropdown = this.newDropdown().hide();

    // Create the button toggle
    var buttonToggle = $('<div></div>')
      .addClass('import-button-toggle')
      .bind('click', this.handleToggleClick)

    // The action button
    var buttonAction = this.getActionButton();

    // Append to root element, effectivly rendering the button
    $(root)
      .html([buttonAction, buttonToggle, dropdown]);

  }.bind(this);

  // Initialize the component
  this.initialize();

  // Do the initial render
  this.render();
};

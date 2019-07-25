# Chorales

This was my senior year techlab project in high school that wrote chorales. It uses a [constraint-satisfaction problem](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem) solver to follow basic part writing rules (no parallel fifths, no parallel octaves, no large jumps for voices other than bass, etc.). It also follows some basic rules about which chords can lead to which other chords, as described here:

![Major chord progressions](img/chordprogmaj.png)

## Getting started

Install the [`lilypond`](http://lilypond.org/) application (which it uses for engraving). If you put the application in a non-standard path (i.e., not `/Applications`) you'll need to update the `bin/lilypond` script in this repo.

Ensure you have [`ghostscript`](http://www.ghostscript.com/) installed. On mac you can install with [`homebrew`](http://brew.sh/index.html) using:

    $ brew install gs

Once the dependencies are installed, you can run the program with:

    $ python src/generate.py

This will generate a PDF called `output.pdf`, where you can see what it wrote:

    $ open output.pdf

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/kddeisz/chorales.

## License

The code is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

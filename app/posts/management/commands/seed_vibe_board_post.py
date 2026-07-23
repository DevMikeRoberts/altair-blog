from django.core.management.base import BaseCommand
from django.utils import timezone
from posts.models import Category, Post


class Command(BaseCommand):
    help = "Seeds the vibe board blog post"

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(
            name="Tech", defaults={"slug": "tech"}
        )

        if Post.objects.filter(slug="the-vibe-board-chronicles").exists():
            self.stdout.write("Post already exists, skipping")
            return

        Post.objects.create(
            title="The Vibe Board Chronicles: How I Let LLMs Do My Job While I Vibe",
            slug="the-vibe-board-chronicles",
            excerpt="I built a command center for dispatching LLMs to do my bidding, and honestly, it's kind of unhinged how well it works.",
            category=category,
            published=True,
            published_at=timezone.now(),
            content="""Look, I'm not saying I'm lazy. I'm saying I've achieved a level of efficiency so advanced that it looks like laziness to the untrained eye. Enter: The Vibe Board.

The Vibe Board is my personal command center for dispatching LLMs to do the actual work of building and maintaining my projects. Think of it as a DJ booth, but instead of dropping beats, I'm dropping prompts that spin up entire microservices, refactor legacy code, and write tests I never would have written myself.

The workflow is dead simple. I open the Vibe Board, vibe check my repos, pick a task, and dispatch it to an LLM with the right context. The LLM does the heavy lifting, I review the PR, and we move on. No context switching. No tab management. No "wait, what was I doing again?" Just vibes.

Here's the thing nobody tells you about AI-assisted development: it's not about the AI writing perfect code. It's about removing the activation energy required to start. The hardest part of any task is the first five minutes. The Vibe Board eliminates those five minutes entirely. You go from "I should probably fix that bug" to "bug is fixed, PR is up, CI is green" without ever leaving the comfort of your vibe.

The lazy part? That's a feature, not a bug. The entire philosophy is: why memorize a codebase when you can just describe what you want and let an LLM figure out the details? Why write boilerplate when a prompt can generate it in three seconds? Why debug for twenty minutes when you can paste an error message and get a fix before your coffee gets cold?

I've been using it to maintain about a dozen projects now. New feature? Dispatch. Dependency update with breaking changes? Dispatch. Documentation that nobody wants to write? You already know. The Vibe Board has turned me from a developer who does everything manually into a developer who orchestrates a small army of language models while occasionally touching grass.

The stack is irrelevant. The framework doesn't matter. What matters is the vibe, and the vibe is: work smarter, not harder. Let the machines handle the grunt work. Save your brain cells for the decisions that actually require a human.

If you're still writing every line of code by hand in 2026, I respect the craft. But also, have you considered vibes?""",
        )

        self.stdout.write(self.style.SUCCESS("Created vibe board blog post"))

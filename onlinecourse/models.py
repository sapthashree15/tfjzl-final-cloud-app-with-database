# ✅ Question model
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.TextField()
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    # Method to check if learner got the score
    def is_get_score(self, selected_choice_ids):
        all_correct = set(self.choice_set.filter(is_correct=True).values_list('id', flat=True))
        selected = set(selected_choice_ids)
        return all_correct.issubset(selected)


# ✅ Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


# ✅ Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id} for enrollment {self.enrollment.id}"

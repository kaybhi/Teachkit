// Homework worksheet PDF — one A4 page + one A4 answer key
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { LOGO_PNG_BASE64, LOGO_ASPECT_RATIO } from "./logoData";

const LIME = [166, 226, 46];
const BLACK = [10, 10, 10];

function header(doc, teacher, subtitle) {
  doc.setFillColor(...BLACK);
  doc.rect(0, 0, 210, 20, "F");
  doc.setFillColor(...LIME);
  doc.rect(0, 20, 210, 1, "F");

  const logoH = 12;
  const logoW = logoH * LOGO_ASPECT_RATIO;
  doc.addImage(LOGO_PNG_BASE64, "PNG", 14, 4, logoW, logoH);

  doc.setTextColor(255, 255, 255);
  doc.setFont("helvetica", "bold");
  doc.setFontSize(14);
  doc.text("[THE] TEACHKIT", 14 + logoW + 3, 12);
  doc.setFont("helvetica", "normal");
  doc.setFontSize(9);
  doc.setTextColor(220, 220, 220);
  if (subtitle) doc.text(subtitle, 196, 12, { align: "right" });
}

export function exportHomeworkPdf(lesson, teacher) {
  const hw = lesson.homework;
  if (!hw) return;
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  header(doc, teacher, `Homework · Week ${lesson.week}`);

  doc.setTextColor(...BLACK);
  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.text(hw.title, 14, 36, { maxWidth: 180 });
  doc.setFontSize(9);
  doc.setTextColor(120, 120, 120);
  doc.text(`Week ${lesson.week} · ~${hw.estimated_minutes || 15} min · CEFR ${lesson.cefr_level}`, 14, 43);
  doc.setFontSize(10);
  doc.setTextColor(...BLACK);
  doc.text("Name: __________________________     Date: ______________", 14, 54);
  doc.setFont("helvetica", "italic");
  const inst = doc.splitTextToSize(hw.instructions_for_student || "", 180);
  doc.text(inst, 14, 62);

  let y = 62 + inst.length * 5 + 4;

  const drawExercise = (ex, num) => {
    if (!ex) return;
    if (y > 240) { doc.addPage(); header(doc, teacher, `Homework · Week ${lesson.week}`); y = 30; }
    doc.setFont("helvetica", "bold");
    doc.setFontSize(12);
    doc.text(`${num}. ${ex.title}`, 14, y);
    doc.setDrawColor(...LIME);
    doc.line(14, y + 1.5, 14 + doc.getTextWidth(`${num}. ${ex.title}`), y + 1.5);
    y += 6;
    doc.setFont("helvetica", "italic");
    doc.setFontSize(9);
    const li = doc.splitTextToSize(ex.instructions || "", 180);
    doc.text(li, 14, y);
    y += li.length * 4 + 2;
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    if (ex.items) {
      ex.items.forEach((it, i) => {
        const lines = doc.splitTextToSize(`${i + 1}. ${it}`, 180);
        doc.text(lines, 14, y);
        y += lines.length * 5;
        doc.setDrawColor(180, 180, 180);
        doc.line(14, y, 194, y);
        y += 6;
      });
    } else if (ex.pairs) {
      autoTable(doc, {
        startY: y,
        head: [["Word", "Definition"]],
        body: ex.pairs.map((p) => [p.word, p.definition]),
        headStyles: { fillColor: LIME, textColor: BLACK },
        styles: { fontSize: 9, cellPadding: 2 },
        columnStyles: { 0: { cellWidth: 50, fontStyle: "bold" }, 1: { cellWidth: 140 } },
      });
      y = doc.lastAutoTable.finalY + 3;
    }
    y += 3;
  };

  drawExercise(hw.exercise_1, 1);
  drawExercise(hw.exercise_2, 2);
  drawExercise(hw.exercise_3, 3);

  if (hw.note_for_parents) {
    if (y > 260) { doc.addPage(); header(doc, teacher, `Homework · Week ${lesson.week}`); y = 30; }
    y += 3;
    doc.setFillColor(240, 250, 210);
    doc.rect(12, y - 2, 186, 14, "F");
    doc.setFont("helvetica", "bold");
    doc.setFontSize(9);
    doc.setTextColor(...BLACK);
    doc.text("Note for the family:", 14, y + 3);
    doc.setFont("helvetica", "italic");
    const np = doc.splitTextToSize(hw.note_for_parents, 180);
    doc.text(np, 14, y + 8);
  }

  doc.save(`teachkit-week-${lesson.week}-homework.pdf`);
}

export function exportHomeworkAnswersPdf(lesson, teacher) {
  const hw = lesson.homework;
  if (!hw?.answer_key) return;
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  header(doc, teacher, `Homework Answer Key · Week ${lesson.week}`);

  doc.setTextColor(...BLACK);
  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.text(`${hw.title} — Answer Key`, 14, 36, { maxWidth: 180 });

  let y = 52;
  const sections = [
    ["Exercise 1", hw.answer_key.exercise_1],
    ["Exercise 2 (sample answers)", hw.answer_key.exercise_2],
    ["Exercise 3", hw.answer_key.exercise_3],
  ];
  sections.forEach(([title, arr]) => {
    if (!arr) return;
    if (y > 250) { doc.addPage(); header(doc, teacher, `Homework Answer Key · Week ${lesson.week}`); y = 30; }
    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.text(title.toUpperCase(), 14, y);
    doc.setDrawColor(...LIME);
    doc.line(14, y + 1.5, 14 + doc.getTextWidth(title.toUpperCase()) + 6, y + 1.5);
    y += 6;
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    arr.forEach((v, i) => {
      const lines = doc.splitTextToSize(`${i + 1}. ${v}`, 180);
      doc.text(lines, 14, y);
      y += lines.length * 5;
    });
    y += 4;
  });

  doc.save(`teachkit-week-${lesson.week}-homework-answers.pdf`);
}
